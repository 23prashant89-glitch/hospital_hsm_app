"""Streamlit components for patient management backed by Google Sheets."""

from __future__ import annotations

from datetime import datetime
import uuid

import pandas as pd
import streamlit as st

from hospital_hms_app.database.connection import (
    append_patient,
    read_patients,
)
from hospital_hms_app.database.schemas import PatientRecord


def _generate_patient_id() -> str:
    return f"PAT-{uuid.uuid4().hex[:8].upper()}"


def _patient_registration_form() -> None:
    st.subheader("Patient Registration")
    with st.form("patient_registration"):
        name = st.text_input("Patient Name", placeholder="e.g. Amit Verma")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
        contact_number = st.text_input("Contact number", placeholder="+91-98765-43210")
        medical_history = st.text_area("Medical history", height=120)
        submitted = st.form_submit_button("Register Patient")

    if submitted:
        if not name:
            st.error("Patient name is required.")
            return
        patient = PatientRecord(
            patient_id=_generate_patient_id(),
            name=name,
            age=str(int(age)),
            gender=gender,
            contact=contact_number,
            medical_history=medical_history or "",
        )
        append_patient(patient)
        st.success(f"Patient {name} registered successfully with ID {patient.patient_id}")


def _active_patients_table() -> None:
    st.subheader("Currently Admitted Patients")
    df = read_patients()
    if df.empty:
        st.info("No patient records available.")
        return

    admitted = df[df["Status"].str.lower() == "admitted"].copy()
    if admitted.empty:
        st.info("No active admitted patients.")
        return

    st.dataframe(admitted, use_container_width=True, hide_index=True)


def render() -> None:
    """Render the patient management workflow."""

    st.title("Patient Management")
    tabs = st.tabs([
        "Registration",
        "Active Patients",
    ])

    with tabs[0]:
        _patient_registration_form()

    with tabs[1]:
        _active_patients_table()

