#!/usr/bin/env python3
"""Validator leggero per la skill cost-aware-app-coordinator.

Esegui dalla root della skill:
    python scripts/validate_skill.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_FILE = ROOT / "SKILL.md"
REFERENCES_DIR = ROOT / "references"
ASSETS_DIR = ROOT / "assets"

# SKILL.md cap: la doc ufficiale Anthropic raccomanda <500 righe per il body;
# 350 lascia margine per future aggiunte e tiene tutta la skill scorrevole.
SKILL_MAX_LINES = 350
# Reference cap: garantisce che ogni reference sia leggibile in un colpo
# d'occhio e che oltre questa soglia la sezione vada spostata o splittata
# (raccomandazione: TOC se >100 righe).
REFERENCE_MAX_LINES = 120
# Limite ufficiale Anthropic per il campo description del frontmatter.
DESCRIPTION_MAX_CHARS = 1024

REQUIRED_FRONTMATTER_KEYS = {"name", "description"}
REQUIRED_SECTIONS = [
    "Lingua",
    "Classificazione del task",
    "Budget mode",
    "Lettura iniziale del contesto",
    "Progressive loading",
    "Working loop",
    "Output economy",
    "Gate decisionali e rischio",
    "Specialisti",
    "Handoff tra agenti",
    "Definition of Done",
    "Validator",
]


def err(messages: list[str], msg: str) -> None:
    messages.append(f"ERRORE: {msg}")


def warn(messages: list[str], msg: str) -> None:
    messages.append(f"WARN:   {msg}")


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    issues: list[str] = []
    if not text.startswith("---\n"):
        err(issues, "frontmatter mancante (deve aprire con ---)")
        return {}, issues
    end = text.find("\n---", 4)
    if end == -1:
        err(issues, "frontmatter non chiuso (--- finale mancante)")
        return {}, issues
    raw = text[4:end]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            err(issues, f"riga frontmatter non valida: {line!r}")
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip()
    missing = REQUIRED_FRONTMATTER_KEYS - data.keys()
    if missing:
        err(issues, f"frontmatter manca le chiavi: {sorted(missing)}")

    name = data.get("name", "")
    if name:
        if len(name) > 64:
            err(issues, f"frontmatter name supera 64 caratteri: {len(name)}")
        if not re.fullmatch(r"[a-z0-9-]+", name):
            err(issues, f"frontmatter name non conforme (solo a-z, 0-9, hyphens): {name!r}")
        if "anthropic" in name or "claude" in name:
            err(issues, f"frontmatter name contiene una reserved word: {name!r}")

    description = data.get("description", "")
    if description and len(description) > DESCRIPTION_MAX_CHARS:
        err(issues, f"frontmatter description supera {DESCRIPTION_MAX_CHARS} caratteri: {len(description)}")

    return data, issues


def find_headings(text: str) -> list[tuple[int, str, str]]:
    headings = []
    in_fence = False
    fence_marker = ""
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            headings.append((i, m.group(1), m.group(2)))
    return headings


def extract_reference_paths(text: str) -> set[str]:
    pattern = re.compile(r"references/([A-Za-z0-9_\-]+\.md)")
    return set(pattern.findall(text))


def extract_asset_paths(text: str) -> set[str]:
    pattern = re.compile(r"assets/([A-Za-z0-9_\-/]+\.[A-Za-z0-9]+)")
    return set(pattern.findall(text))


def check_assets(messages: list[str], skill_text: str) -> None:
    cited = extract_asset_paths(skill_text)
    if not ASSETS_DIR.exists():
        if cited:
            err(messages, f"SKILL.md cita assets/ ma la cartella non esiste: {sorted(cited)}")
        return
    on_disk: set[str] = set()
    for p in ASSETS_DIR.rglob("*"):
        if p.is_file():
            on_disk.add(str(p.relative_to(ASSETS_DIR)).replace("\\", "/"))
    missing = sorted(cited - on_disk)
    if missing:
        err(messages, f"asset citati da SKILL.md ma assenti: {missing}")
    if cited and not missing:
        messages.append(f"OK:     {len(cited)} asset citati esistono in assets/")


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def check_skill(messages: list[str]) -> tuple[str, set[str]]:
    if not SKILL_FILE.exists():
        err(messages, f"SKILL.md non trovato in {SKILL_FILE}")
        return "", set()
    text = SKILL_FILE.read_text(encoding="utf-8")
    lines = line_count(SKILL_FILE)
    if lines > SKILL_MAX_LINES:
        err(messages, f"SKILL.md ha {lines} righe (max {SKILL_MAX_LINES})")
    else:
        messages.append(f"OK:     SKILL.md {lines} righe (<= {SKILL_MAX_LINES})")

    _, fm_issues = parse_frontmatter(text)
    messages.extend(fm_issues)
    if not fm_issues:
        messages.append("OK:     frontmatter valido")

    headings = find_headings(text)
    titles = [h[2].lower() for h in headings]
    seen: dict[str, int] = {}
    for _, _, title in headings:
        key = title.lower()
        seen[key] = seen.get(key, 0) + 1
    duplicates = [t for t, c in seen.items() if c > 1]
    if duplicates:
        err(messages, f"heading duplicati in SKILL.md: {duplicates}")
    else:
        messages.append("OK:     nessun heading duplicato in SKILL.md")

    missing_sections = []
    for section in REQUIRED_SECTIONS:
        if not any(section.lower() in t for t in titles):
            missing_sections.append(section)
    if missing_sections:
        err(messages, f"sezioni obbligatorie mancanti: {missing_sections}")
    else:
        messages.append("OK:     sezioni obbligatorie presenti")

    cited = extract_reference_paths(text)
    return text, cited


def check_references(messages: list[str], cited: set[str]) -> None:
    if not REFERENCES_DIR.exists():
        err(messages, f"cartella references/ non trovata in {REFERENCES_DIR}")
        return
    on_disk = {p.name for p in REFERENCES_DIR.glob("*.md")}

    missing_files = sorted(cited - on_disk)
    if missing_files:
        err(messages, f"reference citate da SKILL.md ma assenti: {missing_files}")

    orphan_files = sorted(on_disk - cited)
    if orphan_files:
        err(
            messages,
            f"reference presenti ma non citate da SKILL.md: {orphan_files}",
        )

    if not missing_files and not orphan_files:
        messages.append(
            f"OK:     {len(on_disk)} reference allineate con SKILL.md"
        )

    for ref in sorted(on_disk):
        path = REFERENCES_DIR / ref
        n = line_count(path)
        if n > REFERENCE_MAX_LINES:
            err(messages, f"references/{ref} ha {n} righe (max {REFERENCE_MAX_LINES})")
        ref_text = path.read_text(encoding="utf-8")
        ref_headings = find_headings(ref_text)
        seen: dict[str, int] = {}
        for _, level, title in ref_headings:
            if len(level) > 2:
                continue
            key = title.lower()
            seen[key] = seen.get(key, 0) + 1
        dupes = [t for t, c in seen.items() if c > 1]
        if dupes:
            err(messages, f"heading duplicati in references/{ref}: {dupes}")


def check_progressive_loading(messages: list[str], skill_text: str) -> None:
    pl_match = re.search(
        r"Progressive loading[\s\S]+?(?=\n## )",
        skill_text,
        re.IGNORECASE,
    )
    if not pl_match:
        err(messages, "sezione 'Progressive loading' non trovata in SKILL.md")
        return
    pl_block = pl_match.group(0)
    pl_refs = extract_reference_paths(pl_block)
    on_disk = {p.name for p in REFERENCES_DIR.glob("*.md")} if REFERENCES_DIR.exists() else set()
    missing = sorted(on_disk - pl_refs)
    if missing:
        err(
            messages,
            f"progressive loading non cita: {missing}",
        )
    else:
        messages.append("OK:     progressive loading copre tutte le reference")


def main() -> int:
    messages: list[str] = []
    skill_text, cited = check_skill(messages)
    if skill_text:
        check_progressive_loading(messages, skill_text)
        check_assets(messages, skill_text)
    check_references(messages, cited)

    errors = [m for m in messages if m.startswith("ERRORE:")]
    warns = [m for m in messages if m.startswith("WARN:")]
    oks = [m for m in messages if m.startswith("OK:")]

    for m in oks:
        print(m)
    for m in warns:
        print(m)
    for m in errors:
        print(m)

    print()
    print(f"Risultato: {len(oks)} ok, {len(warns)} warn, {len(errors)} errori")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
