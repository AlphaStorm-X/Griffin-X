import os
import json
import google.generativeai as genai
from PIL import Image
from database import get_scheduled_medication, PatientData

# Setup Gemini API
def setup_gemini():
    api_key = "AIzaSyCsoJGWemHlqe__37ElFCfz6UL0CwcsPRc"
    genai.configure(api_key=api_key)
    return True

def verify_pill(image_path: str, patient: PatientData, current_time) -> str:
    """
    Verifies a pill held in the patient's hand against their scheduled medication.
    Uses Gemini 3 Flash vision capabilities.
    """
    scheduled_med = get_scheduled_medication(patient.patient_id, current_time)
    
    if not scheduled_med:
        return f"{patient.name}, you do not have any medications scheduled for this time."

    has_api = setup_gemini()
    
    if not has_api:
        # Mock Response
        return (f"{patient.name}, you're holding your {scheduled_med.dosage} "
                f"{scheduled_med.name}. This is the correct dose for your "
                f"{scheduled_med.schedule_time} schedule. You are safe to take it.")

    # Actual Gemini Implementation
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        img = Image.open(image_path)
        
        prompt = f"""
        You are a highly accurate medical assistant. The user is holding a pill in their hand.
        Please analyze this image. Zoom in on the pill, and identify its shape, color, and any imprints or serial numbers.
        
        The expected medication at this time is:
        Name: {scheduled_med.name}
        Dosage: {scheduled_med.dosage}
        Appearance: {scheduled_med.appearance}
        
        Compare the pill in the image with the expected medication. 
        If it matches, generate a comforting, spoken-style confirmation addressing the patient ({patient.name}) directly, stating the medication name, dose, schedule time, and confirming it is safe to take.
        If it does NOT match, generate a firm, spoken-style warning to the patient not to take it and to double-check their prescription.
        """
        
        response = model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        return f"An error occurred during verification: {str(e)}"
