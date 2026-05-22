"""Load profile definitions from profiles.toml."""
from __future__ import annotations

import tomllib
from pathlib import Path


def load_all(path: Path | None = None) -> dict[str, dict]:
    path = path or Path("profiles.toml")
    with path.open("rb") as f:
        return tomllib.load(f)


def load_profile(name: str, path: Path | None = None) -> dict:
    all_profiles = load_all(path)
    if name not in all_profiles:
        raise KeyError(f"unknown profile: {name} (available: {', '.join(sorted(all_profiles))})")
    return all_profiles[name]
