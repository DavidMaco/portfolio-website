"""
Static-site generator — renders Jinja2 templates to flat HTML in dist/.
Usage:  python build.py
"""
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from app.data import load_projects

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
TEMPLATES = ROOT / "app" / "templates"
STATIC = ROOT / "static"


def build():
    # ── Clean dist ──
    if DIST.exists():
        shutil.rmtree(DIST)

    DIST.mkdir(parents=True)
    (DIST / "projects").mkdir()

    # ── Copy static assets ──
    shutil.copytree(STATIC, DIST / "static")

    # ── Set up Jinja2 ──
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=True,
    )

    projects = load_projects()

    # ── Render homepage ──
    index_tmpl = env.get_template("index.html")
    index_html = index_tmpl.render(projects=projects, base="")
    (DIST / "index.html").write_text(index_html, encoding="utf-8")
    print(f"  [ok] index.html")

    # ── Render each project detail page ──
    project_tmpl = env.get_template("project.html")
    for p in projects:
        html = project_tmpl.render(project=p, base="../")
        out_path = DIST / "projects" / f"{p['id']}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"  [ok] projects/{p['id']}.html")

    # ── Create a .nojekyll file (GitHub Pages) ──
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    total = 1 + len(projects)
    print(f"\nBuild complete: {total} pages written to dist/")


if __name__ == "__main__":
    build()
