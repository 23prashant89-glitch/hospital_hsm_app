"""Billing and financial management components using Google Sheets storage."""

from __future__ import annotations

from datetime import datetime
import uuid

import streamlit as st

from hospital_hms_app.database.connection import read_patients


def render() -> None:
    st.title("Billing & Finance")

    st.subheader("Generate Invoice (Sheet Integration Pending)")
    patients_df = read_patients()
    if patients_df.empty:
        st.info("Register patients to create invoices.")
    else:
        st.write("Invoice management can be integrated with Google Sheets similar to other modules.")

    st.subheader("Insurance Claims")
    st.info("Insurance claim workflows can append to a dedicated Google Sheet tab.")

    st.subheader("Payment Integrations")
    st.info("Mock payment gateway callbacks can be simulated via custom Streamlit forms.")

