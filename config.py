"""Streamlit secrets driven configuration for Google Sheets HMS."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict

import streamlit as st


@dataclass(slots=True, frozen=True)
class GoogleSheetsConfig:
    spreadsheet_id: str
    patients_sheet: str
    lab_sheet: str
    discharge_sheet: str


@dataclass(slots=True, frozen=True)
class AppConfig:
    environment: str
    gsheets: GoogleSheetsConfig


def _load_config_from_secrets() -> Dict[str, Any]:
    try:
        return st.secrets["gsheets"]  # type: ignore[index]
    except Exception as exc:  # pragma: no cover - Streamlit handles secrets
        raise RuntimeError(
            "Google Sheets credentials missing. Populate `.streamlit/secrets.toml`"
        ) from exc


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    data = _load_config_from_secrets()
    gsheets = GoogleSheetsConfig(
        spreadsheet_id=data["spreadsheet_id"],
        patients_sheet=data.get("patients_sheet", "Patients"),
        lab_sheet=data.get("lab_sheet", "Lab_Entries"),
        discharge_sheet=data.get("discharge_sheet", "Discharge_Summaries"),
    )
    env = st.secrets.get("environment", {}).get("name", "development")
    return AppConfig(environment=env, gsheets=gsheets)


