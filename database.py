from typing import List, Dict, Optional
from pydantic import BaseModel
import datetime

class Medication(BaseModel):
    id: str
    name: str
    dosage: str
    appearance: str # e.g., "White, round, imprinted '10'"
    schedule_time: str # e.g., "09:00"

class PatientData(BaseModel):
    patient_id: str
    name: str
    medications: List[Medication]
    emergency_contact: str

# Mock Database
MOCK_PATIENTS = {
    "P12345": PatientData(
        patient_id="P12345",
        name="Monika",
        medications=[
            Medication(
                id="M001",
                name="Lisinopril",
                dosage="10mg",
                appearance="White, round pill, imprinted with '10'",
                schedule_time="09:00"
            ),
            Medication(
                id="M002",
                name="Metformin",
                dosage="500mg",
                appearance="White, oblong pill, imprinted with '500'",
                schedule_time="20:00"
            )
        ],
        emergency_contact="+15550199"
    )
}

def get_patient(patient_id: str) -> Optional[PatientData]:
    """Retrieve patient data by ID."""
    return MOCK_PATIENTS.get(patient_id)

def get_scheduled_medication(patient_id: str, current_time: datetime.datetime) -> Optional[Medication]:
    """Find a medication scheduled near the given time (e.g., within +/- 1 hour)."""
    patient = get_patient(patient_id)
    if not patient:
        return None
        
    current_time_str = current_time.strftime("%H:%M")
    
    # Simple mockup: Just returns the first one that somewhat matches the hour,
    # or just returns Lisinopril if it's morning.
    hour = current_time.hour
    for med in patient.medications:
        med_hour = int(med.schedule_time.split(":")[0])
        if abs(hour - med_hour) <= 2:
            return med
            
    return None
