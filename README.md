# David Igbonaju — Portfolio Website

Premium dark-theme portfolio built with **FastAPI + Jinja2** and deployed as a static site on **GitHub Pages**.

## Architecture

```
app/
  main.py          # FastAPI dev server (uvicorn)
  data.py          # YAML data loader
  templates/       # Jinja2 templates (base, index, project)
static/
  css/main.css     # Design system
  js/main.js       # Scroll animations, counters
data/
  projects.yml     # Curated flagship project data
build.py           # Static site generator → dist/
```

## Local Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Build Static Site

```bash
python build.py        # → dist/
```

## Deploy

Push to `main`. GitHub Actions builds and deploys to GitHub Pages automatically.

## Flagship Projects

| Project | Domain | Status |
|---------|--------|--------|
| AEGIS | Procurement Analytics | Production-Ready |
| PVIS | Procurement Analytics | Production-Ready |
| TCO Model | Capital Equipment | Production-Ready |
| Green ROI | Green Procurement | Pilot-Ready |
