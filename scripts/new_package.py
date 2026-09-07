#!/usr/bin/env python3
"""
Scaffold a new packages/<slug>/ folder.

Usage:
    python3 scripts/new_package.py <slug> --name "Display Name" [--version 0.1.0]
"""
import argparse
from pathlib import Path

from _common import PACKAGES_DIR

PACKAGE_YAML_TEMPLATE = """\
name: "{name}"
slug: {slug}
version: {version}
mo2_mod_name: "{name}"

# Shared components/ folders to pull in wholesale (see ../../components/)
includes: []

meta_ini:
  comments: "TODO: one-line summary for MO2's mod info panel"
  notes: "TODO: install order / compat notes"
"""

README_TEMPLATE = """\
# {name}

TODO: one-paragraph description.

## What you should feel

TODO.

## Install

1. Drop this folder (or the built zip) into MO2 / copy into `mods/`.
2. TODO: load-order notes.
3. Restart the game.

## Requirements

- Skyrim SE/AE + SKSE + SkyrimNet
- TODO

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| TODO | TODO |

## Version

{version} — TODO
"""

CHANGELOG_TEMPLATE = """\
# Changelog

All notable changes to this package are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [{version}] - Unreleased

### Added
- Initial scaffold.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--name", required=True)
    parser.add_argument("--version", default="0.1.0")
    args = parser.parse_args()

    pkg_dir = PACKAGES_DIR / args.slug
    if pkg_dir.exists():
        raise SystemExit(f"packages/{args.slug} already exists")

    (pkg_dir / "overlay").mkdir(parents=True)

    (pkg_dir / "package.yaml").write_text(
        PACKAGE_YAML_TEMPLATE.format(name=args.name, slug=args.slug, version=args.version),
        encoding="utf-8",
    )
    (pkg_dir / "README.md").write_text(
        README_TEMPLATE.format(name=args.name, version=args.version), encoding="utf-8"
    )
    (pkg_dir / "CHANGELOG.md").write_text(
        CHANGELOG_TEMPLATE.format(version=args.version), encoding="utf-8"
    )

    print(f"Scaffolded packages/{args.slug}/")


if __name__ == "__main__":
    main()
