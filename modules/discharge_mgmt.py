"""Discharge summary management components leveraging Google Sheets storage."""

from __future__ import annotations

from datetime import datetime
import uuid

import streamlit as st

from hospital_hms_app.database.connection import (
    append_discharge_summary,
    read_patients,
    update_patient_status,
)
from hospital_hms_app.database.schemas import DischargeSummaryRecord


def _generate_discharge_id() -> str:
    return f"DSC-{uuid.uuid4().hex[:8].upper()}"


def render() -> None:
    st.title("Discharge Summary Generator")

    patients_df = read_patients()
    admitted = (
        patients_df[patients_df["Status"].str.lower() == "admitted"]
        if not patients_df.empty
        else patients_df
    )

    if admitted.empty:
        st.info("No admitted patients available for discharge.")
        return

    patient_map = {
        f"{row['Name']} ({row['Patient_ID']})": row["Patient_ID"]
        for _, row in admitted.iterrows()
    }

    with st.form("discharge_form"):
        patient_label = st.selectbox("Patient", list(patient_map.keys()))
        diagnosis = st.text_area("Final Diagnosis", height=120)
        treatment = st.text_area("Treatment Summary", height=120)
        follow_up = st.text_area("Follow-up Advice", height=120)
        emergency_contact = st.text_input("Emergency Contact", placeholder="e.g. +91-90000-00000")
        submitted = st.form_submit_button("Discharge Patient")

    if submitted:
        if not all([diagnosis, treatment, follow_up, emergency_contact]):
            st.error("All discharge summary fields are required.")
            return

        patient_id = patient_map[patient_label]
        record = DischargeSummaryRecord(
            discharge_id=_generate_discharge_id(),
            patient_id=patient_id,
            final_diagnosis=diagnosis,
            treatment_summary=treatment,
            follow_up_advice=follow_up,
            emergency_contacts=emergency_contact,
            discharge_date=datetime.now().strftime("%Y-%m-%d"),
        )
        append_discharge_summary(record)
        updated = update_patient_status(patient_id, "Discharged")
        if updated:
            st.success(f"Discharge summary saved and patient {patient_label} marked as Discharged.")
        else:
            st.warning("Summary saved, but failed to update patient status. Please verify in the sheet.")

