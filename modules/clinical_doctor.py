"""Doctor-facing Streamlit components using Google Sheets data."""

from __future__ import annotations

from datetime import datetime
import uuid

import streamlit as st

from hospital_hms_app.database.connection import read_lab_entries, read_patients


def render() -> None:
    st.title("Clinical & Doctor Dashboard")

    patients = read_patients()
    if patients.empty:
        st.info("No patient records available.")
        return

    admitted = patients[patients["Status"].str.lower() == "admitted"].copy()

    st.subheader("Admitted Patient Queue")
    if admitted.empty:
        st.info("No admitted patients in queue.")
    else:
        st.dataframe(admitted[["Patient_ID", "Name", "Medical_History"]], hide_index=True)

    st.subheader("E-Prescription")
    with st.form("e_prescription"):
        options = {
            f"{row['Name']} ({row['Patient_ID']})": row["Patient_ID"] for _, row in patients.iterrows()
        }
        patient_label = st.selectbox("Patient", list(options.keys()))
        prescription = st.text_area("Prescription", placeholder="List medicines and dosage")
        submitted = st.form_submit_button("Save Prescription")
    if submitted:
        if not prescription:
            st.error("Prescription details are required.")
        else:
            st.success(f"Prescription saved for {patient_label}. (Persist to sheet in future enhancement)")

    st.subheader("Recent Lab Results")
    lab_entries = read_lab_entries()
    if lab_entries.empty:
        st.info("No lab entries recorded yet.")
    else:
        st.dataframe(lab_entries.sort_values(by="Date", ascending=False), hide_index=True)

