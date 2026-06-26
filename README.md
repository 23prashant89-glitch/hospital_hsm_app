# Hospital HMS Streamlit App

## Overview

This project delivers a modular Hospital Management System prototype powered by Streamlit with Google Sheets as the lightweight persistence layer. The Streamlit entry point [`app.py`](hospital_hms_app/app.py) loads configuration from [`config.py`](hospital_hms_app/config.py), presents navigable sidebar sections, and defers feature logic to dedicated modules under [`modules`](hospital_hms_app/modules/__init__.py). Authentication, patient management, laboratory workflows, discharge summaries, and billing touchpoints are implemented with pragmatic, prototype-friendly defaults.

## Feature Highlights

- Navigation and session flow are orchestrated by [`_render_navigation()`](hospital_hms_app/app.py:24), ensuring only authenticated users reach clinical modules after the [`data_security.render_login()`](hospital_hms_app/modules/data_security.py:8) stub establishes `st.session_state` flags.
- Patient intake and status visibility live in [`patient_mgmt.render()`](hospital_hms_app/modules/patient_mgmt.py:63), creating new [`PatientRecord`](hospital_hms_app/database/schemas.py:10) entries and listing active admissions from Google Sheets data.
- The clinical dashboard [`clinical_doctor.render()`](hospital_hms_app/modules/clinical_doctor.py:13) consolidates admitted queues, quick prescriptions, and latest lab results sourced through [`read_lab_entries()`](hospital_hms_app/database/connection.py:139).
- Laboratory workflows in [`lab_pharmacy.render()`](hospital_hms_app/modules/lab_pharmacy.py:61) capture diagnostics via [`append_lab_entry()`](hospital_hms_app/database/connection.py:135) while exposing historical entries.
- Discharge automation handled by [`discharge_mgmt.render()`](hospital_hms_app/modules/discharge_mgmt.py:22) persists summaries, generates IDs, and updates patient status through [`update_patient_status()`](hospital_hms_app/database/connection.py:127).
- Financial placeholders in [`billing_finance.render()`](hospital_hms_app/modules/billing_finance.py:13) outline invoice, insurance, and payment integration stubs ready for future Google Sheets expansion.

## Architecture

| Layer | Components |
| --- | --- |
| UI / Streamlit | [`app.main()`](hospital_hms_app/app.py:60), module-level `render()` implementations |
| Domain Schemas | [`PatientRecord`](hospital_hms_app/database/schemas.py:10), [`LabEntryRecord`](hospital_hms_app/database/schemas.py:32), [`DischargeSummaryRecord`](hospital_hms_app/database/schemas.py:50) |
| Data Access | [`connection.py`](hospital_hms_app/database/connection.py) utilities encapsulating Google Sheets reads, appends, and updates |
| Configuration | [`get_config()`](hospital_hms_app/config.py:35) memoizes Streamlit secrets into structured dataclasses |

### Google Sheets Layout

The helper constant [`HEADER_MAP`](hospital_hms_app/database/connection.py:26) guarantees consistent column ordering across `Patients`, `Lab_Entries`, and `Discharge_Summaries` worksheets. New records rely on GUID-backed helpers (`PAT-`, `LAB-`, `DSC-` prefixes) generated within their respective modules to preserve uniqueness.

## Project Structure

```
hospital_hms_app/
├── app.py
├── config.py
├── database/
│   ├── connection.py
│   └── schemas.py
├── modules/
│   ├── billing_finance.py
│   ├── clinical_doctor.py
│   ├── data_security.py
│   ├── discharge_mgmt.py
│   ├── lab_pharmacy.py
│   └── patient_mgmt.py
└── requirements.txt
```

## Setup

1. **Install dependencies**

   ```bash
   pip install -r hospital_hms_app/requirements.txt
   ```

2. **Provision Streamlit secrets**

   Supply Google service account credentials and sheet metadata in [` .streamlit/secrets.toml`](.streamlit/secrets.toml). The configuration loader [`get_config()`](hospital_hms_app/config.py:35) expects:

   ```toml
   [gcp_service_account]
   type = "service_account"
   # ... remaining service account keys ...

   [gsheets]
   spreadsheet_id = "<GOOGLE_SHEET_ID>"
   patients_sheet = "Patients"
   lab_sheet = "Lab_Entries"
   discharge_sheet = "Discharge_Summaries"

   [environment]
   name = "development"
   ```

   Ensure the service account has edit access to the target spreadsheet.

3. **Bootstrap worksheets**

   The first run auto-seeds column headers defined in [`HEADER_MAP`](hospital_hms_app/database/connection.py:26) for each worksheet. Verify sheet tabs and naming align with the configuration above.

## Running the App

Execute the Streamlit launcher from the repository root:

```bash
streamlit run hospital_hms_app/app.py
```

The top-level [`main()`](hospital_hms_app/app.py:60) sets page metadata, loads environment context, and renders the sidebar navigation. Authenticate via the login form to unlock patient, lab, billing, and discharge modules. Session state can be reset using the logout action in [`render_login()`](hospital_hms_app/modules/data_security.py:8).

## Development Notes

- All Google Sheets calls are memoized or cached where appropriate (`lru_cache` usage in [`_client()`](hospital_hms_app/database/connection.py:55) and [`get_config()`](hospital_hms_app/config.py:35)). Clear the cache when rotating credentials or sheet IDs.
- The codebase favors explicit dataclasses for outbound rows, simplifying future validation or serialization enhancements.
- Extend each module by persisting additional fields into Sheets or by integrating partner APIs; the modular `render()` pattern keeps concerns isolated per feature area.

