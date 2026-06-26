"""Google Sheets connection utilities for HMS."""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, Iterable

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

from hospital_hms_app.config import get_config
from hospital_hms_app.database.schemas import (
    DischargeSummaryRecord,
    LabEntryRecord,
    PatientRecord,
)


REQUIRED_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
]

HEADER_MAP = {
    "Patients": [
        "Patient_ID",
        "Name",
        "Age",
        "Gender",
        "Contact",
        "Medical_History",
        "Status",
    ],
    "Lab_Entries": [
        "Entry_ID",
        "Patient_ID",
        "Test_Name",
        "Test_Result",
        "Date",
    ],
    "Discharge_Summaries": [
        "Discharge_ID",
        "Patient_ID",
        "Final_Diagnosis",
        "Treatment_Summary",
        "FollowUp_Advice",
        "Emergency_Contacts",
        "Discharge_Date",
    ],
}


@lru_cache(maxsize=1)
def _client() -> gspread.Client:
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=REQUIRED_SCOPES
    )
    return gspread.authorize(creds)


def _headers(sheet_name: str) -> list[str]:
    return HEADER_MAP.get(sheet_name, [])


def _ensure_headers(ws: gspread.Worksheet, headers: Iterable[str]) -> None:
    headers_list = list(headers)
    if not headers_list:
        return
    existing = ws.row_values(1)
    if existing[: len(headers_list)] != headers_list:
        ws.update("A1", [headers_list])


def _worksheet(sheet_name: str) -> gspread.Worksheet:
    cfg = get_config()
    client = _client()
    sheet = client.open_by_key(cfg.gsheets.spreadsheet_id)
    ws = sheet.worksheet(sheet_name)
    _ensure_headers(ws, _headers(sheet_name))
    return ws


def _read_dataframe(sheet_name: str) -> pd.DataFrame:
    ws = _worksheet(sheet_name)
    rows = ws.get_all_records()
    df = pd.DataFrame(rows)
    if df.empty:
        df = pd.DataFrame(columns=_headers(sheet_name))
    return df


def _append(sheet_name: str, values: Dict[str, str]) -> None:
    ws = _worksheet(sheet_name)
    headers = _headers(sheet_name)
    row = [values.get(header, "") for header in headers]
    ws.append_row(row, value_input_option="USER_ENTERED")


def _update_row(sheet_name: str, key_column: str, key_value: str, updates: Dict[str, str]) -> bool:
    ws = _worksheet(sheet_name)
    headers = _headers(sheet_name)
    df = pd.DataFrame(ws.get_all_records())
    if df.empty:
        return False
    matches = df[df[key_column].astype(str) == str(key_value)]
    if matches.empty:
        return False
    row_idx = matches.index[0] + 2
    for column, value in updates.items():
        if column not in headers:
            continue
        col_idx = headers.index(column) + 1
        ws.update_cell(row_idx, col_idx, value)
    return True


def read_patients() -> pd.DataFrame:
    return _read_dataframe("Patients")


def append_patient(record: PatientRecord) -> None:
    _append("Patients", record.to_row())


def update_patient_status(patient_id: str, status: str) -> bool:
    return _update_row("Patients", "Patient_ID", patient_id, {"Status": status})


def read_lab_entries() -> pd.DataFrame:
    return _read_dataframe("Lab_Entries")


def append_lab_entry(record: LabEntryRecord) -> None:
    _append("Lab_Entries", record.to_row())


def read_discharge_summaries() -> pd.DataFrame:
    return _read_dataframe("Discharge_Summaries")


def append_discharge_summary(record: DischargeSummaryRecord) -> None:
    _append("Discharge_Summaries", record.to_row())

