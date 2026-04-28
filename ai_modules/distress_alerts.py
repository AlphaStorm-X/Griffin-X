import os
import google.generativeai as genai
from database import PatientData

def setup_gemini():
    api_key = "AIzaSyCsoJGWemHlqe__37ElFCfz6UL0CwcsPRc"
    genai.configure(api_key=api_key)
    return True

def trigger_emergency_alert(patient: PatientData, summary: str):
    """
    Simulates sending an alert to the emergency contact via Firebase Cloud Messaging.
    """
    print(f"\n[ALERT SYSTEM] Sending Firebase Cloud Message...")
    print(f"[ALERT SYSTEM] To: {patient.emergency_contact}")
    print(f"[ALERT SYSTEM] Message: {summary}\n")
    return True

def process_distress_signal(patient: PatientData, signal_type: str, sensor_data: dict) -> str:
    """
    Processes a trigger from on-device ML Kit (e.g., 'fall_detected', 'acoustic_distress').
    Uses Gemini to summarize the situation and sends an alert.
    """
    has_api = setup_gemini()
    
    context = ""
    if signal_type == "fall_detected":
        context = f"High-Impact motion detected. Location: {sensor_data.get('location', 'Unknown')}. Heart rate: {sensor_data.get('heart_rate', 'Unknown')} bpm."
    elif signal_type == "acoustic_distress":
        context = f"Acoustic keywords/sounds detected. Keywords: {sensor_data.get('keywords', 'None')}. Breathing pattern: {sensor_data.get('breathing', 'Unknown')}."
    
    if not has_api:
        summary = f"EMERGENCY: {patient.name}. {context}. Patient requires immediate attention."
        trigger_emergency_alert(patient, summary)
        return summary

    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = f"""
        You are an emergency AI assistant monitoring a patient named {patient.name}.
        The on-device ML Kit has triggered a '{signal_type}' alert.
        Context from sensors: {context}
        
        Generate a very brief, urgent, and clear summary of the situation to be sent as an SMS/Push Notification to the patient's emergency contact.
        It must be factual and emphasize the critical details.
        """
        
        response = model.generate_content(prompt)
        summary = response.text.strip()
        
        trigger_emergency_alert(patient, summary)
        return summary
    except Exception as e:
        error_msg = f"EMERGENCY ALERT FAILED TO GENERATE SUMMARY. RAW DATA: {context}"
        trigger_emergency_alert(patient, error_msg)
        return error_msg
