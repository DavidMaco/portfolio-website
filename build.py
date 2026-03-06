"""
Static-site generator — renders Jinja2 templates to flat HTML in dist/.
Usage:  python build.py
"""
import shutil
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from app.data import load_projects

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
TEMPLATES = ROOT / "app" / "templates"
STATIC = ROOT / "static"
SITE_URL = "https://davidmaco.github.io"


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

    # ── Render 404 page ──
    error_tmpl = env.get_template("404.html")
    error_html = error_tmpl.render(base="")
    (DIST / "404.html").write_text(error_html, encoding="utf-8")
    print(f"  [ok] 404.html")

    # ── Create .nojekyll ──
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    # ── Generate robots.txt ──
    robots = f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"  [ok] robots.txt")

    # ── Generate sitemap.xml ──
    today = datetime.now().strftime("%Y-%m-%d")
    urls = [{"loc": f"{SITE_URL}/", "priority": "1.0"}]
    for p in projects:
        urls.append({"loc": f"{SITE_URL}/projects/{p['id']}.html", "priority": "0.8"})

    sitemap_entries = "\n".join(
        f"  <url>\n    <loc>{u['loc']}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{u['priority']}</priority>\n  </url>"
        for u in urls
    )
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_entries}\n</urlset>\n'
    (DIST / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"  [ok] sitemap.xml")

    total = 1 + len(projects) + 3  # index + projects + 404 + robots + sitemap
    print(f"\nBuild complete: {total} pages/files written to dist/")


if __name__ == "__main__":
    build()
