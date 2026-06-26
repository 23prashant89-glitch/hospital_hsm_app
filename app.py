"""Streamlit entry point for the Hospital Management System."""

from __future__ import annotations

import os
from pathlib import Path
import sys

os.environ.setdefault("NPY_USE_LEGACY_LONGDOUBLE", "1")

import streamlit as st

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from hospital_hms_app.config import get_config
from hospital_hms_app.modules import (
    billing_finance,
    clinical_doctor,
    data_security,
    discharge_mgmt,
    lab_pharmacy,
    patient_mgmt,
)


def _render_navigation() -> None:
    st.sidebar.title("Hospital HMS")
    st.sidebar.caption("Production-ready modular Streamlit HMS")

    navigation = st.sidebar.radio(
        "Navigate",
        options=[
            "Login",
            "Patient Management",
            "Clinical & Doctor",
            "Billing & Finance",
            "Lab & Pharmacy",
            "Discharge Management",
        ],
    )

    if navigation == "Login":
        data_security.render_login()
    else:
        if not st.session_state.get("authenticated"):
            st.warning("Please authenticate via the Login module to access HMS features.")
            data_security.render_login()
            return

        if navigation == "Patient Management":
            patient_mgmt.render()
        elif navigation == "Clinical & Doctor":
            clinical_doctor.render()
        elif navigation == "Billing & Finance":
            billing_finance.render()
        elif navigation == "Lab & Pharmacy":
            lab_pharmacy.render()
        elif navigation == "Discharge Management":
            discharge_mgmt.render()


def main() -> None:
    st.set_page_config(page_title="Hospital HMS", layout="wide", initial_sidebar_state="expanded")
    config = get_config()
    st.sidebar.success(f"Environment: {config.environment.capitalize()}")

    _render_navigation()


if __name__ == "__main__":
    main()

