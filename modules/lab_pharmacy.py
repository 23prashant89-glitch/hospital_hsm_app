"""Laboratory and pharmacy Streamlit components backed by Google Sheets."""

from __future__ import annotations

from datetime import datetime
import uuid

import streamlit as st

from hospital_hms_app.database.connection import append_lab_entry, read_lab_entries, read_patients
from hospital_hms_app.database.schemas import LabEntryRecord


def _generate_entry_id() -> str:
    return f"LAB-{uuid.uuid4().hex[:8].upper()}"


def _book_lab_test() -> None:
    st.subheader("Book Lab Test")
    patients = read_patients()
    active = patients[patients["Status"].str.lower() == "admitted"] if not patients.empty else patients

    if patients.empty or active.empty:
        st.info("Register and admit patients to create lab entries.")
        return

    patient_options = {
        f"{row['Name']} ({row['Patient_ID']})": row["Patient_ID"] for _, row in active.iterrows()
    }

    with st.form("lab_test_form"):
        patient_label = st.selectbox("Patient", list(patient_options.keys()))
        test_name = st.text_input("Test Name", placeholder="e.g. Complete Blood Count")
        test_result = st.text_area("Test Result", placeholder="Enter observations or attach link")
        submitted = st.form_submit_button("Save Lab Entry")

    if submitted:
        if not test_name:
            st.error("Test name is required.")
            return
        record = LabEntryRecord(
            entry_id=_generate_entry_id(),
            patient_id=patient_options[patient_label],
            test_name=test_name,
            test_result=test_result or "Pending",
            date=datetime.now().strftime("%Y-%m-%d"),
        )
        append_lab_entry(record)
        st.success(f"Lab test recorded for {patient_label} with ID {record.entry_id}")


def _lab_history_table() -> None:
    st.subheader("Recent Lab Entries")
    df = read_lab_entries()
    if df.empty:
        st.info("No lab entries recorded yet.")
        return
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)


def render() -> None:
    st.title("Lab & Pharmacy")
    _book_lab_test()
    _lab_history_table()

