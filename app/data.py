"""
Project data loader — reads the curated YAML and returns typed dicts.
"""
from pathlib import Path
import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_projects() -> list[dict]:
    """Return the list of flagship projects from projects.yml."""
    path = DATA_DIR / "projects.yml"
    with open(path, encoding="utf-8") as fh:
        projects: list[dict] = yaml.safe_load(fh)
    return projects


def get_project(project_id: str) -> dict | None:
    """Return a single project by id, or None."""
    for p in load_projects():
        if p["id"] == project_id:
            return p
    return None
