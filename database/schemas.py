"""Schema definitions for Google Sheets backed storage."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(slots=True)
class PatientRecord:
    patient_id: str
    name: str
    age: str
    gender: str
    contact: str
    medical_history: str
    status: str = "Admitted"

    def to_row(self) -> Dict[str, Any]:
        return {
            "Patient_ID": self.patient_id,
            "Name": self.name,
            "Age": self.age,
            "Gender": self.gender,
            "Contact": self.contact,
            "Medical_History": self.medical_history,
            "Status": self.status,
        }


@dataclass(slots=True)
class LabEntryRecord:
    entry_id: str
    patient_id: str
    test_name: str
    test_result: str
    date: str

    def to_row(self) -> Dict[str, Any]:
        return {
            "Entry_ID": self.entry_id,
            "Patient_ID": self.patient_id,
            "Test_Name": self.test_name,
            "Test_Result": self.test_result,
            "Date": self.date,
        }


@dataclass(slots=True)
class DischargeSummaryRecord:
    discharge_id: str
    patient_id: str
    final_diagnosis: str
    treatment_summary: str
    follow_up_advice: str
    emergency_contacts: str
    discharge_date: str

    def to_row(self) -> Dict[str, Any]:
        return {
            "Discharge_ID": self.discharge_id,
            "Patient_ID": self.patient_id,
            "Final_Diagnosis": self.final_diagnosis,
            "Treatment_Summary": self.treatment_summary,
            "FollowUp_Advice": self.follow_up_advice,
            "Emergency_Contacts": self.emergency_contacts,
            "Discharge_Date": self.discharge_date,
        }

