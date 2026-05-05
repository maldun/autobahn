from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


HIGH_RISK_DOMAINS = [
    "common/technologies",
    "common/technology_tags",
    "common/units/equipment",
    "common/units/equipment/modules",
    "common/scripted_effects",
    "common/scripted_triggers",
    "common/ai_strategy",
    "common/ai_templates",
    "common/national_focus",
    "common/ideas",
    "common/special_projects",
    "common/military_industrial_organization",
    "history/countries",
    "history/units",
    "interface/countrytechtreeview.gui",
    "interface/countrytechtreeview.gfx",
    "interface/tank_designer_view.gui",
    "localisation",
]

TARGET_FILES = [
    "common/units/equipment/plane_airframes.txt",
    "common/units/equipment/tank_chassis.txt",
    "common/scripted_effects/00_transfer_technology_effects.txt",
    "common/scripted_effects/01_American Civil War effects.txt",
    "common/scripted_effects/01_American Tech effects.txt",
    "common/technologies/special_forces_doctrine.txt",
    "common/ai_strategy/00_production.txt",
    "common/special_projects/projects/BM_mobile_dockyard_project.txt",
    "interface/tank_designer_view.gui",
    "interface/countrytechtreeview.gui",
    "history/countries/WCA - Workers Congress of America.txt",
    "history/units/00_kr_FNG_naval.txt",
    "game rules/newb.txt",
]

TECH_REF_RE = re.compile(
    r"\b(?:set_technology|has_tech|has_technology)\s*=\s*([A-Za-z0-9_.:-]+)"
)
IDEA_REF_RE = re.compile(
    r"\b(?:has_idea|add_ideas|remove_ideas|swap_ideas|idea|hidden_ideas?)\s*=\s*([A-Za-z0-9_.:-]+)"
)
MODULE_RE = re.compile(r"\bmodule\s*=\s*([A-Za-z0-9_.:-]+)")
SLOT_RE = re.compile(r"\bslot\s*=\s*([A-Za-z0-9_.:-]+)")
NAME_RE = re.compile(r'^\s*name\s*=\s*"([^"]+)"', re.MULTILINE)
PATH_RE = re.compile(r'^\s*path\s*=\s*"([^"]+)"', re.MULTILINE)
SUPPORTED_RE = re.compile(r'^\s*supported_version\s*=\s*"([^"]+)"', re.MULTILINE)
REPLACE_RE = re.compile(r'^\s*replace_path\s*=\s*"([^"]+)"', re.MULTILINE)
REMOTE_ID_RE = re.compile(r'^\s*remote_file_id\s*=\s*"([^"]+)"', re.MULTILINE)


ERROR_PATTERNS = {
    "invalid_tech": re.compile(
        r'^\[(?P<ts>[^\]]+)\]\[[^\]]+\]\[[^\]]+\]: Error: ".*?(?:set_technology|has_tech): Invalid tech: (?P<id>[A-Za-z0-9_.:-]+).*?" in file: "(?P<file>[^"]+)"'
    ),
    "invalid_idea": re.compile(
        r'^\[(?P<ts>[^\]]+)\]\[[^\]]+\]\[[^\]]+\]: Error: "has_idea: (?P<id>[A-Za-z0-9_.:-]+) is not A valid Idea.*?" in file: "(?P<file>[^"]+)"'
    ),
    "invalid_module": re.compile(
        r'^\[(?P<ts>[^\]]+)\]\[[^\]]+\]\[[^\]]+\]: Error: "Invalid module "(?P<id>[^"]+)".*?" in file: "(?P<file>[^"]+)"'
    ),
    "invalid_variant": re.compile(
        r'^\[(?P<ts>[^\]]+)\]\[[^\]]+\]\[[^\]]+\]: Error: "create_equipment_variant.*?variant: (?P<id>[^"]+?)($|,).*?" in file: "(?P<file>[^"]+)"'
    ),
    "undefined_gui": re.compile(
        r'^\[(?P<ts>[^\]]+)\]\[[^\]]+\]\[[^\]]+\]: Error: "Undefined GUI_TYPE: (?P<id>[A-Za-z0-9_.:-]+).*?" in file: "(?P<file>[^"]+)"'
    ),
    "unexpected_token": re.compile(
        r'^\[(?P<ts>[^\]]+)\]\[[^\]]+\]\[[^\]]+\]: Error: "Unexpected token: (?P<id>[^,]+), near line: .*?" in file: "(?P<file>[^"]+)"'
    ),
}


REFERENCE_CONTEXTS = [
    ("common/scripted_effects", TECH_REF_RE),
    ("common/scripted_triggers", TECH_REF_RE),
    ("history/countries", TECH_REF_RE),
    ("history/units", TECH_REF_RE),
    ("common/units/equipment", TECH_REF_RE),
    ("common/ai_strategy", TECH_REF_RE),
    ("common/special_projects", TECH_REF_RE),
    ("common/military_industrial_organization", TECH_REF_RE),
]


EXCLUDE_TOP_LEVEL = {
    "ai_will_do",
    "allowed",
    "archetype",
    "available",
    "bonus",
    "can_convert_from",
    "categories",
    "category",
    "cost",
    "doctrine_technologies",
    "enable_equipments",
    "enable_equipment_modules",
    "enable_subunits",
    "folder",
    "folders",
    "if",
    "modifier",
    "modules",
    "name",
    "on_completion",
    "path",
    "research_cost",
    "show_equipment_icon",
    "start_year",
    "sub_technologies",
    "technologies",
    "technology",
    "xor",
}


@dataclass
class ModRecord:
    order: int
    descriptor_ref: str
    descriptor_path: Path
    name: str = ""
    path: Path | None = None
    supported_version: str | None = None
    replace_paths: list[str] = field(default_factory=list)
    remote_file_id: str | None = None
    high_risk_files: dict[str, list[str]] = field(default_factory=dict)
    descriptor_root_path: Path | None = None

    @property
    def mod_id(self) -> str:
        stem = self.descriptor_path.name
        if stem.endswith(".mod"):
            stem = stem[:-4]
        return stem


def parse_descriptor_text(text: str) -> dict[str, object]:
    return {
        "name": first_match(NAME_RE, text),
        "path": first_match(PATH_RE, text),
        "supported_version": first_match(SUPPORTED_RE, text),
        "replace_paths": REPLACE_RE.findall(text),
        "remote_file_id": first_match(REMOTE_ID_RE, text),
    }


def first_match(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    return match.group(1) if match else None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def load_active_mods(mod_dir: Path, dlc_load_path: Path) -> list[ModRecord]:
    data = json.loads(read_text(dlc_load_path))
    records: list[ModRecord] = []
    for order, descriptor_ref in enumerate(data.get("enabled_mods", []), start=1):
        descriptor_name = Path(descriptor_ref).name
        descriptor_path = mod_dir / descriptor_name
        if not descriptor_path.exists():
            continue
        launcher_meta = parse_descriptor_text(read_text(descriptor_path))
        root = Path(str(launcher_meta["path"]).replace("/", "\\")).resolve() if launcher_meta["path"] else None
        descriptor_root_path = None
        root_meta: dict[str, object] = {}
        if root is not None:
            candidate = root / "descriptor.mod"
            if candidate.exists():
                descriptor_root_path = candidate
                root_meta = parse_descriptor_text(read_text(candidate))
        name = str(launcher_meta.get("name") or root_meta.get("name") or descriptor_name)
        supported_version = str(
            launcher_meta.get("supported_version")
            or root_meta.get("supported_version")
            or ""
        )
        replace_paths = list(dict.fromkeys([
            *list(root_meta.get("replace_paths") or []),
            *list(launcher_meta.get("replace_paths") or []),
        ]))
        records.append(
            ModRecord(
                order=order,
                descriptor_ref=descriptor_ref,
                descriptor_path=descriptor_path,
                name=name,
                path=root,
                supported_version=supported_version or None,
                replace_paths=replace_paths,
                remote_file_id=str(
                    launcher_meta.get("remote_file_id") or root_meta.get("remote_file_id") or ""
                )
                or None,
                descriptor_root_path=descriptor_root_path,
            )
        )
    return records


def summarize_high_risk_files(mod: ModRecord) -> dict[str, list[str]]:
    if mod.path is None or not mod.path.exists():
        return {}
    results: dict[str, list[str]] = {}
    for domain in HIGH_RISK_DOMAINS:
        domain_path = mod.path / Path(domain)
        if domain_path.is_file():
            results[domain] = [domain]
            continue
        if domain_path.exists():
            files = [
                str(path.relative_to(mod.path)).replace("\\", "/")
                for path in domain_path.rglob("*")
                if path.is_file()
            ]
            if files:
                results[domain] = sorted(files)
    return results


def collect_mod_files(mods: list[ModRecord]) -> dict[str, list[tuple[int, str, Path]]]:
    owners: dict[str, list[tuple[int, str, Path]]] = defaultdict(list)
    for mod in mods:
        if mod.path is None or not mod.path.exists():
            continue
        for file in mod.path.rglob("*"):
            if not file.is_file():
                continue
            rel = str(file.relative_to(mod.path)).replace("\\", "/")
            owners[rel].append((mod.order, mod.name, file))
    return owners


def winning_owner(owners: list[tuple[int, str, Path]] | None) -> tuple[int, str, Path] | None:
    if not owners:
        return None
    return max(owners, key=lambda item: item[0])


def extract_definitions(root: Path, rel_glob: str) -> set[str]:
    defined: set[str] = set()
    for path in root.glob(rel_glob):
        if not path.is_file():
            continue
        for line in read_text(path).splitlines():
            match = re.match(r"^\s*([A-Za-z0-9_.:-]+)\s*=\s*\{", line)
            if not match:
                continue
            token = match.group(1)
            if token not in EXCLUDE_TOP_LEVEL:
                defined.add(token)
    return defined


def collect_winning_paths(vanilla_root: Path, mod_owners: dict[str, list[tuple[int, str, Path]]]) -> dict[str, Path]:
    winning: dict[str, Path] = {}
    for rel, owners in mod_owners.items():
        winner = winning_owner(owners)
        if winner:
            winning[rel] = winner[2]
    return winning


def collect_vanilla_paths(vanilla_root: Path) -> dict[str, Path]:
    vanilla: dict[str, Path] = {}
    for path in vanilla_root.rglob("*"):
        if path.is_file():
            vanilla[str(path.relative_to(vanilla_root)).replace("\\", "/")] = path
    return vanilla


def collect_effective_paths(
    vanilla_root: Path,
    mod_owners: dict[str, list[tuple[int, str, Path]]],
    active_mods: list[ModRecord],
) -> dict[str, Path]:
    effective = collect_vanilla_paths(vanilla_root)
    for mod in active_mods:
        if mod.path is None or not mod.path.exists():
            continue
        for file in mod.path.rglob("*"):
            if not file.is_file():
                continue
            rel = str(file.relative_to(mod.path)).replace("\\", "/")
            effective[rel] = file
    return effective


def extract_log_errors(error_log: Path) -> dict[str, dict[str, dict[str, object]]]:
    results: dict[str, dict[str, dict[str, object]]] = {
        key: {} for key in ERROR_PATTERNS
    }
    for line in read_text(error_log).splitlines():
        for error_type, pattern in ERROR_PATTERNS.items():
            match = pattern.match(line)
            if not match:
                continue
            item_id = match.group("id").strip()
            source_file = match.group("file").replace("\\", "/")
            bucket = results[error_type].setdefault(
                item_id,
                {
                    "count": 0,
                    "first_line": line,
                    "source_files": Counter(),
                },
            )
            bucket["count"] += 1
            bucket["source_files"][source_file] += 1
            break
    return results


def flatten_counter(counter: Counter[str]) -> list[tuple[str, int]]:
    return sorted(counter.items(), key=lambda item: (-item[1], item[0]))


def owner_for_path(path_text: str, active_mods: list[ModRecord], vanilla_root: Path) -> str:
    normalized = path_text.replace("\\", "/").lstrip("./")
    for mod in reversed(active_mods):
        if mod.path is None:
            continue
        candidate = mod.path / Path(normalized)
        if candidate.exists():
            if mod.remote_file_id:
                return f"{mod.name} ({mod.remote_file_id})"
            return mod.name
    if (vanilla_root / Path(normalized)).exists():
        return "Vanilla"
    return "Unknown"


def collect_text_references(
    effective_paths: dict[str, Path],
    rel_prefixes: Iterable[tuple[str, re.Pattern[str]]],
) -> dict[str, list[str]]:
    refs: dict[str, list[str]] = defaultdict(list)
    for rel, pattern in rel_prefixes:
        for path_key, path in effective_paths.items():
            if not path_key.startswith(rel + "/") and path_key != rel:
                continue
            text = read_text(path)
            for match in pattern.finditer(text):
                refs[match.group(1)].append(path_key)
    return refs


def collect_variant_blocks(path: Path) -> list[dict[str, object]]:
    lines = read_text(path).splitlines()
    results: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    depth = 0
    for line in lines:
        stripped = line.strip()
        if "create_equipment_variant" in stripped and "=" in stripped and "{" in stripped:
            current = {"path": str(path).replace("\\", "/"), "name": None, "modules": [], "slots": []}
            depth = line.count("{") - line.count("}")
            continue
        if current is None:
            continue
        depth += line.count("{") - line.count("}")
        name_match = re.search(r"\bname\s*=\s*\"([^\"]+)\"", line)
        if name_match and current["name"] is None:
            current["name"] = name_match.group(1)
        for module_match in MODULE_RE.finditer(line):
            current["modules"].append(module_match.group(1))
        for slot_match in SLOT_RE.finditer(line):
            current["slots"].append(slot_match.group(1))
        if depth <= 0:
            results.append(current)
            current = None
    return results


def write_markdown(
    output_dir: Path,
    mods: list[ModRecord],
    error_data: dict[str, dict[str, dict[str, object]]],
    mod_owners: dict[str, list[tuple[int, str, Path]]],
    effective_paths: dict[str, Path],
    vanilla_root: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    mod_table_path = output_dir / "mod_source_map.md"
    with mod_table_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Active Mod Source Map\n\n")
        fh.write("| Order | Display name | ID/local | Root path | Descriptor path | Supported version | replace_path |\n")
        fh.write("| --- | --- | --- | --- | --- | --- | --- |\n")
        for mod in mods:
            mod_id = mod.remote_file_id or mod.mod_id
            fh.write(
                f"| {mod.order} | {escape_pipe(mod.name)} | {escape_pipe(mod_id)} | "
                f"{escape_pipe(str(mod.path) if mod.path else '')} | {escape_pipe(str(mod.descriptor_path))} | "
                f"{escape_pipe(mod.supported_version or '')} | {escape_pipe(', '.join(mod.replace_paths))} |\n"
            )
        fh.write("\n")
        for mod in mods:
            fh.write(f"## {mod.order}. {mod.name}\n\n")
            if not mod.high_risk_files:
                fh.write("No files found in the requested high-risk domains.\n\n")
                continue
            for domain, files in sorted(mod.high_risk_files.items()):
                fh.write(f"- `{domain}`: {len(files)} file(s)\n")
                preview = files[:20]
                for file in preview:
                    fh.write(f"  - `{file}`\n")
                if len(files) > len(preview):
                    fh.write(f"  - `... {len(files) - len(preview)} more`\n")
            fh.write("\n")

    errors_path = output_dir / "extracted_log_errors.md"
    with errors_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Extracted Log Errors\n\n")
        for error_type, items in error_data.items():
            fh.write(f"## {error_type}\n\n")
            if not items:
                fh.write("No matches found.\n\n")
                continue
            fh.write("| ID | Count | Source file(s) | Suspected owner | First log line |\n")
            fh.write("| --- | --- | --- | --- | --- |\n")
            for item_id, payload in sorted(items.items(), key=lambda item: (-item[1]["count"], item[0])):
                source_files = flatten_counter(payload["source_files"])
                source_text = "; ".join(f"{path} ({count})" for path, count in source_files[:3])
                owner = owner_for_path(source_files[0][0], mods, vanilla_root) if source_files else "Unknown"
                fh.write(
                    f"| {escape_pipe(item_id)} | {payload['count']} | {escape_pipe(source_text)} | "
                    f"{escape_pipe(owner)} | {escape_pipe(payload['first_line'])} |\n"
                )
            fh.write("\n")

    ownership_path = output_dir / "file_ownership.md"
    with ownership_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Target File Ownership\n\n")
        for target in TARGET_FILES:
            fh.write(f"## `{target}`\n\n")
            owners = mod_owners.get(target, [])
            if owners:
                fh.write("| Order | Mod | Path |\n")
                fh.write("| --- | --- | --- |\n")
                for order, mod_name, path in sorted(owners, key=lambda item: item[0]):
                    fh.write(f"| {order} | {escape_pipe(mod_name)} | {escape_pipe(str(path))} |\n")
                winner = winning_owner(owners)
                if winner:
                    fh.write(f"\nWinning version: `{winner[1]}` -> `{winner[2]}`\n\n")
            else:
                vanilla_path = vanilla_root / Path(target)
                if vanilla_path.exists():
                    fh.write(f"Only vanilla provides this file: `{vanilla_path}`\n\n")
                else:
                    fh.write("No provider found.\n\n")

    tech_defs = {
        token
        for rel, path in effective_paths.items()
        if rel.startswith("common/technologies/")
        for token in extract_definitions(path.parent.parent.parent, f"{path.parent.relative_to(path.parent.parent.parent)}/*.txt")
    }
    # The line above is intentionally redundant-safe but not especially useful for effective files,
    # so we replace it with a direct pass over effective tech files.
    tech_defs = set()
    idea_defs = set()
    module_defs = set()
    gui_defs = set()
    for rel, path in effective_paths.items():
        text = read_text(path)
        if rel.startswith("common/technologies/"):
            for line in text.splitlines():
                match = re.match(r"^\s*([A-Za-z0-9_.:-]+)\s*=\s*\{", line)
                if match and match.group(1) not in EXCLUDE_TOP_LEVEL:
                    tech_defs.add(match.group(1))
        elif rel.startswith("common/ideas/"):
            for line in text.splitlines():
                match = re.match(r"^\s*([A-Za-z0-9_.:-]+)\s*=\s*\{", line)
                if match and match.group(1) not in {"ideas", "country", "designer", "political_advisor", "tank_manufacturer"}:
                    idea_defs.add(match.group(1))
        elif rel.startswith("common/units/equipment/modules/"):
            for line in text.splitlines():
                match = re.match(r"^\s*([A-Za-z0-9_.:-]+)\s*=\s*\{", line)
                if match:
                    module_defs.add(match.group(1))
        elif rel.startswith("interface/") and rel.endswith((".gui", ".gfx")):
            for line in text.splitlines():
                match = re.match(r"^\s*([A-Za-z0-9_.:-]+)\s*=\s*\{", line)
                if match:
                    gui_defs.add(match.group(1))

    tech_refs = collect_text_references(effective_paths, REFERENCE_CONTEXTS)
    idea_refs = collect_text_references(
        effective_paths,
        [
            ("common/units/equipment", IDEA_REF_RE),
            ("common/technologies", IDEA_REF_RE),
            ("common/scripted_effects", IDEA_REF_RE),
            ("common/scripted_triggers", IDEA_REF_RE),
            ("history/countries", IDEA_REF_RE),
            ("common/ai_strategy", IDEA_REF_RE),
            ("common/national_focus", IDEA_REF_RE),
        ],
    )

    tech_audit_path = output_dir / "consistency_audit.md"
    with tech_audit_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Consistency Audit\n\n")
        fh.write(f"- Effective technology definitions detected: {len(tech_defs)}\n")
        fh.write(f"- Effective idea definitions detected: {len(idea_defs)}\n")
        fh.write(f"- Effective equipment module definitions detected: {len(module_defs)}\n")
        fh.write(f"- Effective GUI type definitions detected: {len(gui_defs)}\n\n")

        fh.write("## Undefined technology references\n\n")
        undefined_techs = {key: value for key, value in tech_refs.items() if key not in tech_defs}
        if undefined_techs:
            fh.write("| Tech ID | Reference count | Example files |\n")
            fh.write("| --- | --- | --- |\n")
            for tech_id, refs in sorted(undefined_techs.items(), key=lambda item: (-len(item[1]), item[0])):
                examples = "; ".join(sorted(set(refs))[:5])
                fh.write(f"| {escape_pipe(tech_id)} | {len(refs)} | {escape_pipe(examples)} |\n")
        else:
            fh.write("No undefined technology references were detected by the text scan.\n")
        fh.write("\n")

        fh.write("## Undefined idea references\n\n")
        undefined_ideas = {key: value for key, value in idea_refs.items() if key not in idea_defs}
        if undefined_ideas:
            fh.write("| Idea ID | Reference count | Example files |\n")
            fh.write("| --- | --- | --- |\n")
            for idea_id, refs in sorted(undefined_ideas.items(), key=lambda item: (-len(item[1]), item[0])):
                examples = "; ".join(sorted(set(refs))[:5])
                fh.write(f"| {escape_pipe(idea_id)} | {len(refs)} | {escape_pipe(examples)} |\n")
        else:
            fh.write("No undefined idea references were detected by the text scan.\n")
        fh.write("\n")

        fh.write("## Variant blocks touching modules/slots\n\n")
        variant_rows: list[dict[str, object]] = []
        for rel, path in effective_paths.items():
            if rel.startswith("history/") or rel.startswith("common/"):
                variant_rows.extend(collect_variant_blocks(path))
        if variant_rows:
            fh.write("| Variant name | File | Modules | Slots |\n")
            fh.write("| --- | --- | --- | --- |\n")
            for row in variant_rows[:200]:
                fh.write(
                    f"| {escape_pipe(str(row.get('name') or '(unnamed)'))} | {escape_pipe(str(row['path']))} | "
                    f"{escape_pipe(', '.join(row['modules'][:10]))} | {escape_pipe(', '.join(row['slots'][:10]))} |\n"
                )
            if len(variant_rows) > 200:
                fh.write(f"\nTruncated after 200 variant blocks out of {len(variant_rows)}.\n")
        else:
            fh.write("No `create_equipment_variant` blocks were detected.\n")
        fh.write("\n")

        fh.write("## Undefined GUI types from log\n\n")
        gui_errors = error_data.get("undefined_gui", {})
        if gui_errors:
            fh.write("| GUI type | Defined in effective interface set? |\n")
            fh.write("| --- | --- |\n")
            for gui_id in sorted(gui_errors):
                fh.write(f"| {escape_pipe(gui_id)} | {'yes' if gui_id in gui_defs else 'no'} |\n")
        else:
            fh.write("No undefined GUI type entries were parsed from `error.log`.\n")


def escape_pipe(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hoi4-user-dir", required=True)
    parser.add_argument("--hoi4-install-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    user_dir = Path(args.hoi4_user_dir)
    install_dir = Path(args.hoi4_install_dir)
    output_dir = Path(args.output_dir)
    mod_dir = user_dir / "mod"
    dlc_load_path = user_dir / "dlc_load.json"
    error_log = user_dir / "logs" / "error.log"

    mods = load_active_mods(mod_dir, dlc_load_path)
    for mod in mods:
        mod.high_risk_files = summarize_high_risk_files(mod)

    mod_owners = collect_mod_files(mods)
    effective_paths = collect_effective_paths(install_dir, mod_owners, mods)
    error_data = extract_log_errors(error_log)

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "mod_source_map.json"
    json_payload = [
        {
            "order": mod.order,
            "descriptor_ref": mod.descriptor_ref,
            "name": mod.name,
            "root_path": str(mod.path) if mod.path else None,
            "descriptor_path": str(mod.descriptor_path),
            "supported_version": mod.supported_version,
            "replace_path": mod.replace_paths,
            "remote_file_id": mod.remote_file_id,
            "high_risk_domains": {key: len(value) for key, value in mod.high_risk_files.items()},
        }
        for mod in mods
    ]
    json_path.write_text(json.dumps(json_payload, indent=2), encoding="utf-8")

    write_markdown(output_dir, mods, error_data, mod_owners, effective_paths, install_dir)


if __name__ == "__main__":
    main()
