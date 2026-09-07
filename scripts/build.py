#!/usr/bin/env python3
"""
Compose a package's components + overlay into an MO2-mod-shaped folder under dist/.

Usage:
    python3 scripts/build.py <slug>
    python3 scripts/build.py --all

Output:
    dist/<slug>-v<version>/          <- point MO2 at this directly to test, no zip needed
"""
import argparse
import shutil
import sys
from pathlib import Path

from _common import (
    COMPONENTS_DIR,
    PACKAGES_DIR,
    load_package,
    dist_dir_for,
    copytree_merge,
    render_meta_ini,
)


def _merge_includes(includes, dest, slug):
    for component_name in includes:
        component_path = COMPONENTS_DIR / component_name
        if not component_path.exists():
            sys.exit(f"[{slug}] unknown component: {component_name}")
        copytree_merge(component_path, dest)


def _copy_package_markdown(pkg_dir, dest):
    for md in pkg_dir.glob("*.md"):
        if md.name.lower() == "changelog.md":
            continue
        shutil.copy2(md, dest / md.name)


def build_fomod(manifest, pkg_dir, out_dir):
    """
    Zip layout MO2's FOMOD installer expects:

        fomod/info.xml
        fomod/ModuleConfig.xml
        common/SKSE/...          <- always installed
        <option>/SKSE/...        <- one of the SelectExactlyOne plugins
    """
    fomod_src = pkg_dir / "fomod"
    if not (fomod_src / "ModuleConfig.xml").exists():
        sys.exit(f"[{manifest['slug']}] layout: fomod but missing fomod/ModuleConfig.xml")
    copytree_merge(fomod_src, out_dir / "fomod")

    common = out_dir / "common"
    common.mkdir(parents=True)
    _merge_includes(manifest.get("required_includes", []), common, manifest["slug"])
    copytree_merge(pkg_dir / "overlay", common)
    meta = render_meta_ini(manifest)
    (common / "meta.ini").write_text(meta, encoding="utf-8")
    (out_dir / "meta.ini").write_text(meta, encoding="utf-8")
    _copy_package_markdown(pkg_dir, common)

    for option in manifest.get("fomod_options", []):
        opt_id = option["id"]
        dest = out_dir / opt_id
        dest.mkdir(parents=True)
        _merge_includes(option.get("includes", []), dest, manifest["slug"])


def build_one(slug):
    manifest = load_package(slug)
    pkg_dir = manifest["_pkg_dir"]
    out_dir = dist_dir_for(manifest)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    if manifest.get("layout") == "fomod":
        build_fomod(manifest, pkg_dir, out_dir)
    else:
        _merge_includes(manifest.get("includes", []), out_dir, slug)
        copytree_merge(pkg_dir / "overlay", out_dir)
        (out_dir / "meta.ini").write_text(render_meta_ini(manifest), encoding="utf-8")
        _copy_package_markdown(pkg_dir, out_dir)

    print(f"[{slug}] built -> {out_dir}")
    return out_dir


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", nargs="?", help="package slug under packages/")
    parser.add_argument("--all", action="store_true", help="build every package")
    args = parser.parse_args()

    if args.all:
        for pkg_dir in sorted(PACKAGES_DIR.iterdir()):
            if (pkg_dir / "package.yaml").exists():
                build_one(pkg_dir.name)
        return

    if not args.slug:
        parser.error("pass a slug, or --all")

    build_one(args.slug)


if __name__ == "__main__":
    main()
