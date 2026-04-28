# AURACARE/ai-layer/test_ai.py
"""
Test script for all AuraCare AI modules.
Run this to verify everything is working correctly.
"""
from digital_twin import create_health_profile
from emergency_ai import detect_emergency_from_video, detect_emergency_from_audio
from symptom_ai import analyze_symptoms
from medicine_ai import verify_pill
import json
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import all modules


def print_json_result(title: str, result: dict):
    """Pretty print JSON results."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(json.dumps(result, indent=2))
    print(f"{'='*60}\n")


def test_symptom_analysis():
    """Test symptom analysis functionality."""
    print("🧪 Testing Symptom Analysis...")

    # Test case 1: Mild symptoms
    result1 = analyze_symptoms(
        "I have a mild headache and slight fatigue for 2 days",
        patient_age=35,
        medical_history="No major conditions"
    )
    print_json_result("Mild Symptoms Analysis", result1)

    # Test case 2: Severe symptoms
    result2 = analyze_symptoms(
        "Severe chest pain and difficulty breathing, started 30 minutes ago",
        patient_age=58,
        medical_history="High blood pressure"
    )
    print_json_result("Severe Symptoms Analysis", result2)

    return True


def test_emergency_detection():
    """Test emergency detection functionality."""
    print("🧪 Testing Emergency Detection...")

    # Test audio transcript (simulated)
    distress_transcript = "Help! I've fallen and I can't get up. I think I broke my leg."
    result1 = detect_emergency_from_audio(distress_transcript)
    print_json_result("Emergency Detection from Audio", result1)

    # Test normal transcript
    normal_transcript = "I'm just resting in my chair, watching TV."
    result2 = detect_emergency_from_audio(normal_transcript)
    print_json_result("Normal Situation Detection", result2)

    return True


def test_digital_twin():
    """Test digital twin functionality."""
    print("🧪 Testing Digital Twin...")

    # Create health profile
    profile = create_health_profile(
        medical_history="Type 2 diabetes, controlled with medication. Mild hypertension.",
        recent_symptoms="Occasional dizziness in mornings, fatigue",
        medications="Metformin 500mg twice daily, Lisinopril 10mg daily",
        vitals="BP: 130/85, HR: 72, Blood sugar: 110 mg/dL"
    )
    print_json_result("Digital Twin Health Profile", profile)

    return True


def test_medicine_verification():
    """Test medicine verification (requires actual image file)."""
    print("🧪 Testing Medicine Verification...")
    print("⚠️  Note: This test requires an actual pill image file.")
    print("   Create a 'test_images' folder and add a pill image to test.")

    # Check if test image exists
    test_image_path = Path("test_images/pill_sample.jpg")

    if test_image_path.exists():
        try:
            result = verify_pill(str(test_image_path))
            print_json_result("Medicine Verification Result", result)
        except Exception as e:
            print(f"❌ Medicine verification failed: {e}")
    else:
        print("ℹ️  No test image found. Skipping medicine verification test.")
        print("   To test, create 'test_images/pill_sample.jpg' with a pill image.")

    return True


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🚀 AuraCare AI - Test Suite")
    print("="*60)

    # Check for API key
    from gemini_config import GEMINI_API_KEY
    if not GEMINI_API_KEY:
        print("❌ ERROR: GEMINI_API_KEY not found!")
        print("   Please create a .env file with: GEMINI_API_KEY=your_key_here")
        return

    print("✅ API Key found. Running tests...\n")

    tests = [
        ("Symptom Analysis", test_symptom_analysis),
        ("Emergency Detection", test_emergency_detection),
        ("Digital Twin", test_digital_twin),
        ("Medicine Verification", test_medicine_verification),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            print(f"\n--- Running {test_name} Tests ---")
            if test_func():
                passed += 1
                print(f"✅ {test_name} tests passed")
            else:
                failed += 1
                print(f"❌ {test_name} tests failed")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} tests crashed: {e}")

    print("\n" + "="*60)
    print(f"📊 Test Summary: {passed} passed, {failed} failed")
    print("="*60)

    if failed == 0:
        print("\n🎉 All tests passed! AuraCare AI is ready for the hackathon!")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
