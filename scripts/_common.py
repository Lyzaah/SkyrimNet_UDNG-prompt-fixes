"""Shared helpers for the mod-dev build scripts."""
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit(
        "PyYAML is required. Install with: pip install --user pyyaml"
    )

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPONENTS_DIR = REPO_ROOT / "components"
PACKAGES_DIR = REPO_ROOT / "packages"
DIST_DIR = REPO_ROOT / "dist"


def load_package(slug):
    pkg_dir = PACKAGES_DIR / slug
    manifest_path = pkg_dir / "package.yaml"
    if not manifest_path.exists():
        sys.exit(f"No such package: {slug} (missing {manifest_path})")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    manifest["_pkg_dir"] = pkg_dir
    return manifest


def dist_dir_for(manifest):
    return DIST_DIR / f"{manifest['slug']}-v{manifest['version']}"


def copytree_merge(src, dst):
    """Copy src/** into dst/**, overwriting files, without requiring dst to be absent."""
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        return
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def render_meta_ini(manifest):
    meta = manifest.get("meta_ini", {})
    lines = [
        "[General]",
        "gameName=SkyrimSE",
        "modid=0",
        f"version={manifest['version']}",
        f"comments={meta.get('comments', '')}",
        f"notes={meta.get('notes', '')}",
    ]
    return "\n".join(lines) + "\n"
