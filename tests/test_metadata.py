from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]


def test_readme_discovery_sections():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for section in (
        "## At a Glance",
        "## Install",
        "## Verified Quickstart",
        "## Runtime, Data, and Network Boundary",
        "## Limitations",
        "## Publication Status",
        "## Next Action",
    ):
        assert section in readme


def test_pyproject_discovery_metadata():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    assert project["readme"] == "README.md"
    assert project["authors"][0]["email"] == "opensource@auraone.ai"
    assert {"opentelemetry", "otlp", "redaction"} <= set(project["keywords"])
    assert {"Source", "Documentation", "Issues", "Changelog", "Security", "Data Contract"} <= set(project["urls"])
