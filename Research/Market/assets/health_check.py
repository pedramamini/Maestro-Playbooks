#!/usr/bin/env python3
"""
health_check.py -- validator for a market research vault.

Config-driven: entity types, folders, required fields, enumerations, typed
relations and the event ledger all come from kb.yaml, which 1_ANALYZE fills
in once the market survey says what that market needs. The one convention
baked into this file is the funding-consistency check, which looks for the
standard company fields (total_funding, latest_round_size, all_investors)
and skips itself when they are not declared.

A vault of markdown cards has no schema enforcement of its own, so integrity
has to be asserted from outside. This is that assertion. Two failures in
particular poison every downstream rollup while looking fine on the page:
typed relations that point at cards which do not exist, and event state that
records a deal or approval as final when it has only been reported. Both are
checked here.

Run it after every research loop. 5_PROGRESS uses --fail-on critical as a
blocking exit condition, so a run cannot finish while the corpus is broken.

Usage:
    python3 health_check.py                      # validate, print summary
    python3 health_check.py --vault ../myvault   # point at a vault
    python3 health_check.py --report Reports/    # write a dated markdown report
    python3 health_check.py --dedup              # near-duplicate names only
    python3 health_check.py --json               # machine-readable
    python3 health_check.py --fail-on critical   # non-zero exit for CI

Exit codes: 0 clean (or only issues below --fail-on), 1 issues at/above
--fail-on, 2 configuration or vault error (kb.yaml missing or invalid,
PyYAML not installed, a relation targeting an undeclared entity type).
5_PROGRESS treats exit 2 as "integrity unknown", never as "clean".
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("CONFIG ERROR: PyYAML required:  pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def config_error(msg: str):
    print(f"CONFIG ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


# --------------------------------------------------------------------------
# severity
# --------------------------------------------------------------------------
# CRITICAL breaks queries or corrupts reported figures. MEDIUM is sloppiness
# that degrades the corpus. LOW is a queue to work through, not a defect.
CRITICAL, MEDIUM, LOW = "CRITICAL", "MEDIUM", "LOW"
SEVERITY_ORDER = {CRITICAL: 0, MEDIUM: 1, LOW: 2}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Legal suffixes stripped before duplicate comparison. A card named "Acme" and
# one named "Acme, Inc." are the same company and must collide.
LEGAL_SUFFIXES = {
    "inc", "llc", "ltd", "limited", "corp", "corporation", "co", "company",
    "gmbh", "ag", "sa", "sas", "bv", "nv", "plc", "oy", "ab", "as", "aps",
    "pty", "srl", "spa", "kk", "pte", "holdings", "group", "labs", "technologies",
}


class Issue:
    __slots__ = ("severity", "kind", "card", "detail")

    def __init__(self, severity, kind, card, detail):
        self.severity = severity
        self.kind = kind
        self.card = card
        self.detail = detail

    def as_dict(self):
        return {
            "severity": self.severity,
            "kind": self.kind,
            "card": self.card,
            "detail": self.detail,
        }


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def normalize_name(name: str) -> str:
    """Fold a name to a comparison key for duplicate detection."""
    s = str(name).lower()
    s = re.sub(r"[^\w\s]", " ", s)              # punctuation -> space
    parts = s.split()
    # Strip legal suffixes from the END only. "The Company Store" keeps its
    # middle word; "Acme Holdings Inc" loses both trailing ones.
    while len(parts) > 1 and parts[-1] in LEGAL_SUFFIXES:
        parts.pop()
    return " ".join(parts)


def clean_ref(value) -> str:
    """
    Relations are sometimes written as wikilinks or with a folder prefix.
    Reduce any of [[Folder/Name|Alias]], Folder/Name, Name to the bare name.
    """
    s = str(value).strip()
    if s.startswith("[[") and s.endswith("]]"):
        s = s[2:-2]
    if "|" in s:
        s = s.split("|", 1)[0]
    if "/" in s:
        s = s.rsplit("/", 1)[1]
    return s.strip()


def as_list(value):
    """Frontmatter arrays sometimes arrive as a bare scalar. Normalize."""
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def to_date(raw):
    """
    Coerce a frontmatter value to a date, or return None if it is not one.
    datetime is checked first because it is a subclass of date, and a
    datetime compared against date.today() raises TypeError.
    """
    if isinstance(raw, datetime):
        return raw.date()
    if isinstance(raw, date):
        return raw
    if isinstance(raw, str) and DATE_RE.match(raw):
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def parse_frontmatter(path: Path):
    """
    Return (frontmatter_dict, body_str). Frontmatter is None if absent,
    "PARSE_ERROR" if present but invalid YAML, "READ_ERROR" if the file
    could not be read at all.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        return "READ_ERROR", str(e)
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw = text[3:end]
    body = text[end + 4:]
    try:
        fm = yaml.safe_load(raw)
    except yaml.YAMLError:
        return "PARSE_ERROR", body
    return (fm if isinstance(fm, dict) else None), body


# --------------------------------------------------------------------------
# the checker
# --------------------------------------------------------------------------
class HealthCheck:
    def __init__(self, vault: Path, config: dict):
        self.vault = vault
        self.cfg = config
        self.settings = config.get("settings", {}) or {}
        self.enums = config.get("enums", {}) or {}
        self.entities = config.get("entities", {}) or {}
        self.issues: list[Issue] = []

        # cards[etype][canonical_name] = {"path":.., "fm":.., "body":..}
        self.cards: dict[str, dict[str, dict]] = defaultdict(dict)
        # every typed edge, for orphan detection
        self.edges_out: dict[tuple, int] = defaultdict(int)
        self.edges_in: dict[tuple, int] = defaultdict(int)
        self.stats: dict[str, int] = {}
        self.validate_config()

    # ---- config sanity ----
    def validate_config(self):
        """
        kb.yaml is hand-edited by 1_ANALYZE, which is told to prune entity
        types the market does not need. A relation left pointing at a pruned
        type used to crash the relation pass with a KeyError; now it is a
        configuration error with the fix spelled out.
        """
        problems = []
        for etype, spec in self.entities.items():
            if not isinstance(spec, dict) or not spec.get("dir") or not spec.get("key"):
                problems.append(f"entity '{etype}' must declare 'dir' and 'key'.")
                continue
            for field, rspec in (spec.get("relations", {}) or {}).items():
                target = (rspec or {}).get("to")
                if target not in self.entities:
                    problems.append(
                        f"relation {etype}.{field} targets undeclared entity type "
                        f"'{target}'. Declare the type under entities: or remove "
                        f"the relation.")
                mirror = (rspec or {}).get("mirror")
                if mirror and target in self.entities:
                    if mirror not in (self.entities[target].get("relations", {}) or {}):
                        problems.append(
                            f"relation {etype}.{field} declares mirror '{mirror}' "
                            f"but {target} has no relation named '{mirror}'.")
            for field, enum_name in (spec.get("enums", {}) or {}).items():
                if enum_name not in self.enums:
                    problems.append(
                        f"{etype}.{field} references enum '{enum_name}' which is "
                        f"not defined under enums:.")
        led = self.cfg.get("ledger")
        if led:
            if led.get("entity") not in self.entities:
                problems.append(
                    f"ledger.entity '{led.get('entity')}' is not a declared entity type.")
            for k in ("state_field", "terminal_state", "date_field",
                      "counterparty_closed", "counterparty_open"):
                if not led.get(k):
                    problems.append(f"ledger.{k} is required when a ledger block is present.")
        if problems:
            config_error("kb.yaml has problems:\n  - " + "\n  - ".join(problems))

    # ---- reporting ----
    def add(self, severity, kind, card, detail):
        self.issues.append(Issue(severity, kind, card, detail))

    # ---- load ----
    def load(self):
        for etype, spec in self.entities.items():
            folder = self.vault / spec.get("dir", "")
            if not folder.is_dir():
                self.add(MEDIUM, "missing-folder", spec.get("dir", etype),
                         f"Entity type '{etype}' declares dir '{spec.get('dir')}' "
                         f"which does not exist.")
                continue

            key_field = spec.get("key")
            for path in sorted(folder.glob("*.md")):
                rel = str(path.relative_to(self.vault))
                fm, body = parse_frontmatter(path)

                if fm == "READ_ERROR":
                    self.add(CRITICAL, "unreadable", rel,
                             f"File could not be read: {body}")
                    continue
                if fm == "PARSE_ERROR":
                    self.add(CRITICAL, "yaml-parse", rel,
                             "Frontmatter is not valid YAML.")
                    continue
                if fm is None:
                    self.add(CRITICAL, "no-frontmatter", rel,
                             "Card has no YAML frontmatter block.")
                    continue

                stem = path.stem
                declared = fm.get(key_field)
                if declared is None:
                    self.add(CRITICAL, "missing-key", rel,
                             f"Missing key field '{key_field}'. "
                             f"Falling back to filename '{stem}'.")
                elif str(declared).strip() != stem:
                    self.add(MEDIUM, "key-filename-mismatch", rel,
                             f"{key_field}='{declared}' does not match filename "
                             f"'{stem}'. The filename is canonical; relations "
                             f"referencing this card will use '{stem}'.")

                self.cards[etype][stem] = {"path": rel, "fm": fm, "body": body}

        self.stats = {et: len(c) for et, c in self.cards.items()}
        self.stats["total"] = sum(len(c) for c in self.cards.values())

    # ---- field-level checks ----
    def check_fields(self):
        universal = self.settings.get("universal_required", []) or []
        review_below = self.settings.get("relevance_review_below", 30)

        for etype, spec in self.entities.items():
            required = list(universal) + list(spec.get("required", []) or [])
            enum_map = spec.get("enums", {}) or {}
            date_fields = spec.get("dates", []) or []
            money_fields = spec.get("money", []) or []

            for name, card in self.cards[etype].items():
                fm, rel = card["fm"], card["path"]

                # required
                for field in required:
                    val = fm.get(field)
                    if val is None or (isinstance(val, str) and not val.strip()):
                        self.add(CRITICAL, "missing-required", rel,
                                 f"Missing required field '{field}'.")

                # relevance is the field the whole method rests on, so it gets
                # its own validation rather than riding along as a plain int.
                if "relevance" in fm:
                    rv = fm["relevance"]
                    if not isinstance(rv, int) or isinstance(rv, bool):
                        self.add(CRITICAL, "relevance-type", rel,
                                 f"relevance must be an integer 0-100, got {rv!r}.")
                    elif not 0 <= rv <= 100:
                        self.add(CRITICAL, "relevance-range", rel,
                                 f"relevance must be 0-100, got {rv}.")
                    elif rv < review_below:
                        self.add(LOW, "relevance-review", rel,
                                 f"relevance={rv} is below the review threshold "
                                 f"({review_below}). Decide: raise with evidence, "
                                 f"or remove.")
                notes = fm.get("relevance_notes")
                if notes is not None and len(str(notes).strip()) < 20:
                    self.add(MEDIUM, "relevance-notes-thin", rel,
                             "relevance_notes is too short to justify the score. "
                             "Name the specific evidence and the specific doubt.")

                # enums
                for field, enum_name in enum_map.items():
                    if field not in fm or fm[field] is None:
                        continue
                    allowed = self.enums.get(enum_name)
                    if not allowed:
                        continue
                    for v in as_list(fm[field]):
                        if v not in allowed:
                            self.add(MEDIUM, "enum-violation", rel,
                                     f"{field}='{v}' is not in enum '{enum_name}'. "
                                     f"Allowed: {', '.join(map(str, allowed))}.")

                # dates
                today = date.today()
                for field in date_fields:
                    if field not in fm or fm[field] is None:
                        continue
                    raw = fm[field]
                    parsed = to_date(raw)
                    if parsed is None:
                        if isinstance(raw, str) and DATE_RE.match(raw):
                            self.add(MEDIUM, "date-invalid", rel,
                                     f"{field}='{raw}' is not a real date.")
                        else:
                            self.add(MEDIUM, "date-format", rel,
                                     f"{field}='{raw}' is not YYYY-MM-DD.")
                        continue
                    if parsed > today:
                        self.add(MEDIUM, "date-future", rel,
                                 f"{field}='{parsed}' is in the future.")

                # money
                for field in money_fields:
                    if field not in fm or fm[field] is None:
                        continue
                    v = fm[field]
                    if isinstance(v, bool) or not isinstance(v, int):
                        self.add(MEDIUM, "money-format", rel,
                                 f"{field}={v!r} must be a plain integer in "
                                 f"{self.settings.get('currency', 'USD')} "
                                 f"(no symbols, commas or M/B suffixes).")

    # ---- relations ----
    def check_relations(self):
        for etype, spec in self.entities.items():
            relations = spec.get("relations", {}) or {}
            for name, card in self.cards[etype].items():
                fm, rel = card["fm"], card["path"]
                src = (etype, name)

                for field, rspec in relations.items():
                    if field not in fm or fm[field] is None:
                        continue
                    target_type = rspec.get("to")
                    kind = rspec.get("kind", "list")
                    soft = bool(rspec.get("soft", False))
                    values = as_list(fm[field])

                    if kind == "scalar" and len(values) > 1:
                        self.add(MEDIUM, "relation-arity", rel,
                                 f"'{field}' is declared scalar but holds "
                                 f"{len(values)} values.")

                    for raw in values:
                        target = clean_ref(raw)
                        if not target:
                            continue
                        if target in self.cards.get(target_type, {}):
                            self.edges_out[src] += 1
                            self.edges_in[(target_type, target)] += 1
                        else:
                            tdir = self.entities.get(target_type, {}).get("dir", target_type)
                            if soft:
                                # A soft relation may name an entity that has no
                                # card yet. It is a queue item for discovery, not
                                # a broken graph: the People and Capital sweeps
                                # exist to resolve exactly these.
                                self.add(MEDIUM, "unresolved-relation", rel,
                                         f"{field} -> '{target}' has no card in "
                                         f"{tdir}/ yet. Log it in SWEEP_GAPS.md so "
                                         f"discovery picks it up.")
                            else:
                                self.add(CRITICAL, "broken-relation", rel,
                                         f"{field} -> '{target}' has no card in "
                                         f"{tdir}/. Create it, fix the name, or "
                                         f"remove the relation.")

    def check_mirrors(self):
        """
        A mirrored pair stored on both ends must agree, or the graph
        contradicts itself depending on which direction you traverse.
        """
        for etype, spec in self.entities.items():
            for field, rspec in (spec.get("relations", {}) or {}).items():
                mirror = rspec.get("mirror")
                if not mirror:
                    continue
                target_type = rspec.get("to")
                mirror_spec = self.entities.get(target_type, {})
                if mirror not in (mirror_spec.get("relations", {}) or {}):
                    continue

                for name, card in self.cards[etype].items():
                    for raw in as_list(card["fm"].get(field)):
                        target = clean_ref(raw)
                        tcard = self.cards.get(target_type, {}).get(target)
                        if not tcard:
                            continue  # already reported as broken-relation
                        back = {clean_ref(v)
                                for v in as_list(tcard["fm"].get(mirror))}
                        if name not in back:
                            self.add(MEDIUM, "mirror-mismatch", tcard["path"],
                                     f"{card['path']} declares {field} -> "
                                     f"'{target}', but '{target}' does not list "
                                     f"'{name}' in '{mirror}'.")

    # ---- ledger state ----
    def check_ledger_state(self):
        """
        The acquisition-state rules. These are enforced hard because getting
        them wrong silently corrupts every consolidation figure: a rumored
        deal counted as closed inflates both the deal count and the dollar
        total, and nobody notices until someone checks a specific deal.
        """
        led = self.cfg.get("ledger")
        if not led:
            return
        etype = led.get("entity")
        if etype not in self.cards:
            return

        state_f = led.get("state_field")
        terminal = led.get("terminal_state")
        date_f = led.get("date_field")
        closed_f = led.get("counterparty_closed")
        open_f = led.get("counterparty_open")
        status_terminal = terminal  # e.g. "closed"
        # Optional coupling to the card's lifecycle field. For M&A that is
        # status: acquired; for a licensing market it might be status: licensed.
        # Omit status_field in kb.yaml and these checks are skipped.
        lifecycle_f = led.get("status_field")
        lifecycle_terminal = led.get("status_terminal_value")
        open_states = set(as_list(led.get("open_states")) or [])
        reported_f = led.get("reported_date_field")

        for name, card in self.cards[etype].items():
            fm, rel = card["fm"], card["path"]
            state = fm.get(state_f)
            has_closed = fm.get(closed_f) is not None
            has_open = fm.get(open_f) is not None
            has_date = fm.get(date_f) is not None
            status = fm.get(lifecycle_f) if lifecycle_f else None

            if has_closed and state != status_terminal:
                self.add(CRITICAL, "ledger-state", rel,
                         f"'{closed_f}' is set but {state_f}='{state}'. "
                         f"'{closed_f}' is reserved for closed deals; an "
                         f"unclosed one belongs in '{open_f}'.")

            if has_closed and has_open:
                self.add(CRITICAL, "ledger-state", rel,
                         f"Both '{closed_f}' and '{open_f}' are set. A deal is "
                         f"either closed or it is not.")

            if state == status_terminal:
                if not has_closed:
                    self.add(CRITICAL, "ledger-state", rel,
                             f"{state_f}='{terminal}' but '{closed_f}' is missing.")
                if not has_date:
                    self.add(CRITICAL, "ledger-state", rel,
                             f"{state_f}='{terminal}' but '{date_f}' (the close "
                             f"date) is missing.")
                if (lifecycle_f and lifecycle_terminal and status is not None
                        and status != lifecycle_terminal):
                    self.add(CRITICAL, "ledger-state", rel,
                             f"{state_f}='{terminal}' but {lifecycle_f}='{status}'. "
                             f"A terminal event means {lifecycle_f}: "
                             f"{lifecycle_terminal}.")

            if state in open_states:
                if has_date:
                    self.add(CRITICAL, "ledger-state", rel,
                             f"{state_f}='{state}' but '{date_f}' is set. That "
                             f"field means the terminal date; leave it empty "
                             f"until the event is final.")
                if lifecycle_f and lifecycle_terminal and status == lifecycle_terminal:
                    self.add(CRITICAL, "ledger-state", rel,
                             f"{state_f}='{state}' but {lifecycle_f}="
                             f"'{lifecycle_terminal}'. Never set the terminal "
                             f"lifecycle value without a confirmed final event.")

            # rumor aging
            stale_days = led.get("rumor_stale_days")
            reported = fm.get(reported_f) if reported_f else None
            if state in open_states and reported and stale_days:
                rd = to_date(reported)
                if rd is not None:
                    age = (date.today() - rd).days
                    if age > stale_days:
                        self.add(LOW, "rumor-stale", rel,
                                 f"Rumor reported {age} days ago with no movement "
                                 f"(threshold {stale_days}). Note the staleness in "
                                 f"the body; do not delete the trail.")

    # ---- funding consistency ----
    def check_funding(self):
        for etype, spec in self.entities.items():
            money = spec.get("money", []) or []
            if "total_funding" not in money:
                continue
            for name, card in self.cards[etype].items():
                fm, rel = card["fm"], card["path"]
                tf = fm.get("total_funding")
                if tf is None:
                    continue
                if not isinstance(tf, (int, float)) or isinstance(tf, bool):
                    continue
                if tf == 0:
                    if not (fm.get("funding_stage") or fm.get("bootstrapped")
                            or fm.get("corporate_project") or fm.get("public_company")):
                        self.add(MEDIUM, "funding-consistency", rel,
                                 "total_funding=0 but no funding_stage, "
                                 "bootstrapped, corporate_project or "
                                 "public_company flag explains why.")
                else:
                    latest = fm.get("latest_round_size")
                    if isinstance(latest, (int, float)) and latest > tf:
                        self.add(MEDIUM, "funding-consistency", rel,
                                 f"latest_round_size ({latest:,.0f}) exceeds "
                                 f"total_funding ({tf:,.0f}).")
                    if not fm.get("all_investors"):
                        self.add(LOW, "funding-consistency", rel,
                                 f"total_funding={tf:,.0f} but all_investors is "
                                 f"empty.")

    # ---- orphans ----
    def check_orphans(self):
        for etype in self.entities:
            for name, card in self.cards[etype].items():
                key = (etype, name)
                if self.edges_out[key] == 0 and self.edges_in[key] == 0:
                    self.add(MEDIUM, "orphan", card["path"],
                             "No typed relations in or out. Either genuinely "
                             "peripheral, or under-researched. Decide which.")

    # ---- duplicates ----
    def check_duplicates(self):
        """
        Reports near-duplicates; deliberately never merges. A false merge is
        far more expensive to undo than a false positive is to dismiss.
        """
        for etype in self.entities:
            buckets = defaultdict(list)
            for name, card in self.cards[etype].items():
                buckets[normalize_name(name)].append((name, card["path"]))
            for norm, members in buckets.items():
                if len(members) > 1:
                    names = ", ".join(f"'{n}'" for n, _ in members)
                    self.add(CRITICAL, "duplicate-name", members[0][1],
                             f"{len(members)} cards normalize to '{norm}': "
                             f"{names}. Merge, or disambiguate both filenames.")

    # ---- staleness ----
    def check_staleness(self):
        window = self.settings.get("staleness_days")
        if not window:
            return
        today = date.today()
        for etype in self.entities:
            for name, card in self.cards[etype].items():
                d = to_date(card["fm"].get("last_updated"))
                if d is None:
                    continue
                age = (today - d).days
                if age > window:
                    self.add(LOW, "stale", card["path"],
                             f"last_updated {age} days ago (window {window}). "
                             f"Queue for the freshness sweep.")

    # ---- run ----
    def run(self):
        self.load()
        self.check_fields()
        self.check_relations()
        self.check_mirrors()
        self.check_ledger_state()
        self.check_funding()
        self.check_orphans()
        self.check_duplicates()
        self.check_staleness()
        self.issues.sort(key=lambda i: (SEVERITY_ORDER[i.severity], i.kind, i.card))
        return self.issues

    # ---- relevance distribution: the scope-drift signal ----
    def relevance_distribution(self):
        bands = {"90-100": 0, "70-89": 0, "50-69": 0, "30-49": 0, "0-29": 0,
                 "unscored": 0}
        total, count = 0, 0
        for etype in self.entities:
            for card in self.cards[etype].values():
                v = card["fm"].get("relevance")
                if not isinstance(v, int) or isinstance(v, bool):
                    bands["unscored"] += 1
                    continue
                total += v
                count += 1
                if v >= 90:   bands["90-100"] += 1
                elif v >= 70: bands["70-89"] += 1
                elif v >= 50: bands["50-69"] += 1
                elif v >= 30: bands["30-49"] += 1
                else:         bands["0-29"] += 1
        bands["mean"] = round(total / count, 1) if count else None
        return bands

    # ---- budget: how many cards count against MAX_ENTITIES ----
    def budget_cards(self) -> int:
        excluded = set(as_list(self.settings.get("budget_exclude_types")) or [])
        return sum(n for et, n in self.stats.items()
                   if et != "total" and et not in excluded)

    def lowest_coverage(self):
        """(etype, field, pct) for the least-covered tracked field, or None."""
        worst = None
        for etype, counts in self.field_coverage().items():
            for f, (filled, total) in counts.items():
                pct = round(100 * filled / total) if total else 0
                if worst is None or pct < worst[2]:
                    worst = (etype, f, pct)
        return worst

    # ---- field coverage: what the next sweep should target ----
    def field_coverage(self):
        """
        Per entity type, how many cards carry each declared field. 4_RESEARCH
        reads this as the sweep queue: the lowest-coverage field is the next
        column worth sweeping.

        Conditional fields are excluded, and that exclusion is what makes the
        queue usable. A field like `acquisition_amount` is empty on almost
        every card because almost no company has been acquired -- that is the
        correct state, not a gap. Ranking it as 0% coverage would send the
        next sweep chasing a field that cannot be filled, every single loop.
        Declare such fields under `coverage_exclude` in kb.yaml.
        """
        out = {}
        for etype, spec in self.entities.items():
            cards = self.cards[etype]
            if not cards:
                continue
            tracked = set(spec.get("required", []) or [])
            tracked |= set((spec.get("enums", {}) or {}).keys())
            tracked |= set(spec.get("dates", []) or [])
            tracked |= set(spec.get("money", []) or [])
            tracked |= set((spec.get("relations", {}) or {}).keys())
            tracked |= set(spec.get("tracked", []) or [])
            tracked |= set(self.settings.get("universal_required", []) or [])
            tracked -= set(spec.get("coverage_exclude", []) or [])
            counts = {}
            for f in sorted(tracked):
                filled = sum(1 for c in cards.values()
                             if c["fm"].get(f) not in (None, "", []))
                counts[f] = (filled, len(cards))
            out[etype] = counts
        return out


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------
def render_markdown(hc: HealthCheck, issues) -> str:
    by_sev = defaultdict(list)
    for i in issues:
        by_sev[i.severity].append(i)
    by_kind = defaultdict(int)
    for i in issues:
        by_kind[i.kind] += 1

    L = []
    A = L.append
    A(f"# Health Check - {date.today().isoformat()}")
    A("")
    A(f"**Domain:** {hc.cfg.get('domain', '(unset)')}  ")
    A(f"**Vault:** `{hc.vault}`")
    A("")

    A("## Corpus")
    A("")
    A("| Entity | Cards |")
    A("|---|---|")
    for etype in hc.entities:
        A(f"| {etype} | {hc.stats.get(etype, 0)} |")
    A(f"| **total** | **{hc.stats.get('total', 0)}** |")
    A(f"| **counts against MAX_ENTITIES** | **{hc.budget_cards()}** |")
    A("")

    dist = hc.relevance_distribution()
    A("## Relevance distribution")
    A("")
    A("Watch the mean run over run. A falling mean means the boundary is eroding.")
    A("")
    A("| Band | Cards |")
    A("|---|---|")
    for band in ("90-100", "70-89", "50-69", "30-49", "0-29", "unscored"):
        A(f"| {band} | {dist[band]} |")
    A(f"| **mean** | **{dist['mean']}** |")
    A("")

    A("## Issues")
    A("")
    if not issues:
        A("None. Corpus is clean.")
        A("")
    else:
        A("| Severity | Count |")
        A("|---|---|")
        for sev in (CRITICAL, MEDIUM, LOW):
            A(f"| {sev} | {len(by_sev[sev])} |")
        A(f"| **total** | **{len(issues)}** |")
        A("")
        A("| Kind | Count |")
        A("|---|---|")
        for kind, n in sorted(by_kind.items(), key=lambda x: -x[1]):
            A(f"| {kind} | {n} |")
        A("")

        for sev in (CRITICAL, MEDIUM, LOW):
            if not by_sev[sev]:
                continue
            A(f"### {sev}")
            A("")
            grouped = defaultdict(list)
            for i in by_sev[sev]:
                grouped[i.kind].append(i)
            for kind in sorted(grouped):
                A(f"**{kind}** ({len(grouped[kind])})")
                A("")
                for i in grouped[kind]:
                    A(f"- `{i.card}` - {i.detail}")
                A("")

    A("## Field coverage")
    A("")
    A("The lowest-coverage field is the next column sweep.")
    A("")
    for etype, counts in hc.field_coverage().items():
        A(f"### {etype}")
        A("")
        A("| Field | Filled | Total | % |")
        A("|---|---|---|---|")
        for f, (filled, total) in sorted(counts.items(), key=lambda x: x[1][0]):
            pct = round(100 * filled / total) if total else 0
            A(f"| {f} | {filled} | {total} | {pct}% |")
        A("")

    A("---")
    A("")
    A("Work order: broken relations, then orphans, then missing required fields,")
    A("then enum/format, then ledger state, then duplicates, then the relevance")
    A("review queue. Fixing relations first prevents false orphan reports.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Validate a market knowledge base.")
    ap.add_argument("--vault", default=".", help="vault root (default: cwd)")
    ap.add_argument("--config", default=None, help="path to kb.yaml")
    ap.add_argument("--report", default=None, help="write markdown report to this dir")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--dedup", action="store_true", help="duplicate names only")
    ap.add_argument("--fail-on", choices=["critical", "medium", "low"],
                    default=None, help="non-zero exit at/above this severity")
    args = ap.parse_args()

    vault = Path(args.vault).resolve()
    if not vault.is_dir():
        config_error(f"vault is not a directory: {vault}")
    cfg_path = Path(args.config) if args.config else vault / "kb.yaml"
    if not cfg_path.is_file():
        config_error(f"config not found: {cfg_path}")
    try:
        config = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        config_error(f"kb.yaml is not valid YAML: {e}")
    if not isinstance(config, dict) or "entities" not in config:
        config_error("kb.yaml must define an 'entities' block.")

    hc = HealthCheck(vault, config)

    if args.dedup:
        hc.load()
        hc.issues = []
        hc.check_duplicates()
        if not hc.issues:
            print("No near-duplicate names.")
            return 0
        for i in hc.issues:
            print(f"{i.severity:8} {i.card}: {i.detail}")
        return 1

    issues = hc.run()

    if args.json:
        print(json.dumps({
            "date": date.today().isoformat(),
            "domain": config.get("domain"),
            "stats": hc.stats,
            "budget_cards": hc.budget_cards(),
            "lowest_coverage": hc.lowest_coverage(),
            "critical": sum(1 for i in issues if i.severity == CRITICAL),
            "relevance": hc.relevance_distribution(),
            "coverage": {k: {f: list(v) for f, v in c.items()}
                         for k, c in hc.field_coverage().items()},
            "issues": [i.as_dict() for i in issues],
        }, indent=2))
    else:
        report = render_markdown(hc, issues)
        if args.report:
            out = Path(args.report)
            out.mkdir(parents=True, exist_ok=True)
            fp = out / f"health_check_{date.today().isoformat()}.md"
            fp.write_text(report, encoding="utf-8")
            print(f"Report written: {fp}")

        counts = defaultdict(int)
        for i in issues:
            counts[i.severity] += 1
        print(f"\n{config.get('domain', 'vault')} - {hc.stats.get('total', 0)} cards "
              f"({hc.budget_cards()} count against MAX_ENTITIES)")
        print(f"  CRITICAL {counts[CRITICAL]}   MEDIUM {counts[MEDIUM]}   "
              f"LOW {counts[LOW]}")
        dist = hc.relevance_distribution()
        print(f"  mean relevance: {dist['mean']}   unscored: {dist['unscored']}")
        low = hc.lowest_coverage()
        if low:
            print(f"  lowest coverage: {low[0]}.{low[1]} at {low[2]}%")
        if not args.report and issues:
            print("\nTop issues:")
            for i in issues[:15]:
                print(f"  [{i.severity}] {i.card}: {i.detail}")
            if len(issues) > 15:
                print(f"  ... {len(issues) - 15} more. Use --report or --json.")

    if args.fail_on:
        threshold = SEVERITY_ORDER[args.fail_on.upper()]
        if any(SEVERITY_ORDER[i.severity] <= threshold for i in issues):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
