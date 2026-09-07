#!/usr/bin/env python3
"""
Zip a built package's dist/<slug>-v<version>/ into an MO2-droppable zip.

The zip root contains README.md / meta.ini / SKSE/... directly, with NO
wrapping folder -- this matches every real shipped NEFARAM zip inspected
during the port (04.a, 05, etc).

Usage:
    python3 scripts/package_zip.py <slug>
    python3 scripts/package_zip.py --all

Requires the package to already be built (run scripts/build.py first;
this script will build it if dist/<slug>-v<version>/ is missing).
"""
import argparse
import zipfile
from pathlib import Path

from _common import PACKAGES_DIR, DIST_DIR, load_package, dist_dir_for
from build import build_one


def zip_one(slug):
    manifest = load_package(slug)
    out_dir = dist_dir_for(manifest)
    if not out_dir.exists():
        build_one(slug)

    zips_dir = DIST_DIR / "zips"
    zips_dir.mkdir(parents=True, exist_ok=True)

    mod_name = manifest.get("mo2_mod_name", manifest["slug"])
    zip_path = zips_dir / f"{mod_name}-v{manifest['version']}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in sorted(out_dir.rglob("*")):
            if item.is_file():
                zf.write(item, item.relative_to(out_dir))

    print(f"[{slug}] zipped -> {zip_path}")
    return zip_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", nargs="?")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.all:
        for pkg_dir in sorted(PACKAGES_DIR.iterdir()):
            if (pkg_dir / "package.yaml").exists():
                zip_one(pkg_dir.name)
        return

    if not args.slug:
        parser.error("pass a slug, or --all")

    zip_one(args.slug)


if __name__ == "__main__":
    main()
