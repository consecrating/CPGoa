#!/usr/bin/env python3
"""
Shared WordPress configuration for Casino Pride (cpofficial.in) scripts.

Loads credentials from environment variables (or a local .env file) so that
secrets are NEVER hardcoded in source or committed to git.

Setup:
    1. Copy .env.example to .env
    2. Fill in your WordPress application password
    3. The .env file is gitignored and stays local

Environment variables:
    WP_URL           Base site URL (default: https://www.cpofficial.in)
    WP_USER          WordPress username
    WP_APP_PASSWORD  WordPress application password (WP Admin > Users > Profile)
"""

import base64
import os
from pathlib import Path


def _load_dotenv() -> None:
    """Minimal .env loader (no external dependency).

    Looks for a .env file next to this module and in the repo root, and loads
    any KEY=VALUE pairs that are not already set in the environment.
    """
    candidates = [
        Path(__file__).resolve().parent / ".env",
        Path(__file__).resolve().parents[2] / ".env",
    ]
    for env_path in candidates:
        if not env_path.is_file():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # Do not override variables already present in the real environment.
            os.environ.setdefault(key, value)


_load_dotenv()

WP_URL = os.environ.get("WP_URL", "https://www.cpofficial.in").rstrip("/")
WP_USER = os.environ.get("WP_USER", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")


def require_credentials() -> None:
    """Fail fast with a helpful message if credentials are missing.

    Call this at the start of any script that writes to WordPress.
    """
    missing = [
        name
        for name, value in (("WP_USER", WP_USER), ("WP_APP_PASSWORD", WP_APP_PASSWORD))
        if not value
    ]
    if missing:
        raise SystemExit(
            "Missing WordPress credentials: "
            + ", ".join(missing)
            + "\n\nSet them via environment variables or a local .env file:\n"
            "  cp .env.example .env   # then edit .env\n\n"
            "Get an application password from WP Admin > Users > Profile > "
            "Application Passwords."
        )


def auth_headers() -> dict:
    """Return HTTP Basic auth headers for the WordPress REST API."""
    require_credentials()
    token = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }
