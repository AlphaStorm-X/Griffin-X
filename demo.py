import os
import datetime
from database import get_patient
from ai_modules.pill_verification import verify_pill
from ai_modules.symptom_journal import analyze_symptom_audio, analyze_symptom_image
from ai_modules.distress_alerts import process_distress_signal

def main():
    print("="*50)
    print(" AuraCare: Multimodal Health Guardian Demo ")
    print("="*50)
    
    # 1. Setup
    patient = get_patient("P12345")
    if not patient:
        print("Error: Mock patient not found.")
        return
        
    print(f"\nWelcome, {patient.name}! Initializing AuraCare...")

    # 2. Agentic Vision: Pill Verification Demo
    print("\n--- Feature 1: Agentic Vision (Pill Verification) ---")
    print("Simulating user taking 9:00 AM medication...")
    
    # Simulate time as 09:15 AM
    current_time = datetime.datetime.now().replace(hour=9, minute=15)
    
    # Using a dummy path for image since we rely on mocked response if no API key or image
    dummy_image_path = "dummy_pill.jpg" 
    
    # In a real scenario, this would pass the actual image from the camera
    verification_response = verify_pill(dummy_image_path, patient, current_time)
    print(f"\nAuraCare Voice: \"{verification_response}\"")


    # 3. Multimodal Symptom Journal Demo
    print("\n--- Feature 2: Multimodal Symptom Journal ---")
    print("Simulating user uploading an audio clip of a cough...")
    
    dummy_audio_path = "cough_sample.mp3"
    clinical_snapshot_audio = analyze_symptom_audio(dummy_audio_path)
    print("\nGenerated Clinical Snapshot (Audio):")
    print(clinical_snapshot_audio)
    
    print("\nSimulating user uploading an image of a wound...")
    dummy_wound_image = "wound_day3.jpg"
    clinical_snapshot_visual = analyze_symptom_image(dummy_wound_image)
    print("\nGenerated Clinical Snapshot (Visual):")
    print(clinical_snapshot_visual)


    # 4. Predictive Distress Alerts Demo
    print("\n--- Feature 3: Predictive Distress Alerts ---")
    print("Simulating on-device ML Kit detecting a fall...")
    
    fall_sensor_data = {
        "location": "Kitchen",
        "heart_rate": "115"
    }
    
    process_distress_signal(patient, "fall_detected", fall_sensor_data)
    
    print("\nSimulating on-device ML Kit detecting acoustic distress ('Help')...")
    acoustic_sensor_data = {
        "keywords": "'Help', 'Can't breathe'",
        "breathing": "Labored, rapid"
    }
    
    process_distress_signal(patient, "acoustic_distress", acoustic_sensor_data)
    
    print("\n" + "="*50)
    print(" Demo Complete ")
    print("="*50)

if __name__ == "__main__":
    main()
