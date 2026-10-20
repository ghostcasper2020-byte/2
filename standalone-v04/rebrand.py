#!/usr/bin/env python3
"""Non-invasive, reproducible branding of pinned TLocation source.

This does not change Apple's developer-service protocol or remove Wi-Fi requirements.
TLocation/StikDebug remains credited in source and covered by AGPL-3.0.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

UPSTREAM_SHA = "5e57f815e5958f133dfbaae8252473054adeccf0"
DISPLAY_NAME = "PersonalGPS"
BUNDLE_ID = "com.personal.gps.standalone.v04"


def update_project(upstream: Path) -> None:
    project = upstream / "TLocation.xcodeproj" / "project.pbxproj"
    if not project.is_file():
        raise FileNotFoundError(f"Expected upstream Xcode project missing: {project}")

    contents = project.read_text(encoding="utf-8")
    replacements = {
        "INFOPLIST_KEY_CFBundleDisplayName = TLocation;":
            f"INFOPLIST_KEY_CFBundleDisplayName = {DISPLAY_NAME};",
        "PRODUCT_BUNDLE_IDENTIFIER = vn.truongkma.tlocation;":
            f"PRODUCT_BUNDLE_IDENTIFIER = {BUNDLE_ID};",
    }
    for old, new in replacements.items():
        occurrences = contents.count(old)
        if occurrences != 2:
            raise ValueError(
                f"Unexpected upstream format: expected 2 occurrences of {old!r}, found {occurrences}. "
                "Stop rather than modifying unverified source."
            )
        contents = contents.replace(old, new)

    project.write_text(contents, encoding="utf-8")

    # Display name and privacy prompts may be overridden by the Xcode string catalog.
    catalog = upstream / "TLocation" / "InfoPlist.xcstrings"
    if not catalog.is_file():
        raise FileNotFoundError(f"Expected upstream localization catalog missing: {catalog}")
    data = json.loads(catalog.read_text(encoding="utf-8"))
    names_updated = 0
    for key, entry in data.get("strings", {}).items():
        for localization in entry.get("localizations", {}).values():
            string_unit = localization.get("stringUnit", {})
            value = string_unit.get("value")
            if not isinstance(value, str):
                continue
            if key in {"CFBundleDisplayName", "CFBundleName"}:
                if value != "TLocation":
                    raise ValueError(f"Unexpected {key} localization: {value!r}")
                string_unit["value"] = DISPLAY_NAME
                names_updated += 1
            elif key.startswith("NS") and "TLocation" in value:
                string_unit["value"] = value.replace("TLocation", DISPLAY_NAME)
    if names_updated < 2:
        raise ValueError("No localized display-name entries were updated")
    catalog.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {names_updated} localized display-name entries")
    print(f"Rebranded display name: {DISPLAY_NAME}")
    print(f"Separate bundle ID: {BUNDLE_ID}")
    print("Device engine, pairing, VPN, and source license remain unchanged.")
    print("Cellular-only simulation is NOT claimed to work on iOS 26.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("upstream", type=Path, help="Path to pinned TLocation source")
    args = parser.parse_args()
    update_project(args.upstream)


if __name__ == "__main__":
    main()
