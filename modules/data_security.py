"""Simplified authentication stub for Google Sheets prototype."""

from __future__ import annotations

import streamlit as st


def render_login() -> None:
    st.title("Prototype Login")

    if st.session_state.get("authenticated"):
        st.success("You are already authenticated.")
        if st.button("Logout"):
            st.session_state.clear()
        return

    with st.form("login_form"):
        username = st.text_input("Username", value="demo@hospital.local")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if username and password:
            st.session_state["authenticated"] = True
            st.session_state["user_role"] = "doctor"
            st.success("Demo login successful. RBAC checks are mocked for prototype.")
        else:
            st.error("Enter both username and password to proceed.")

