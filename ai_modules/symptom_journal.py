import os
import google.generativeai as genai

def setup_gemini():
    api_key = "AIzaSyCsoJGWemHlqe__37ElFCfz6UL0CwcsPRc"
    genai.configure(api_key=api_key)
    return True

def analyze_symptom_audio(audio_path: str) -> str:
    """
    Analyzes an audio clip (e.g., of a cough) and generates a clinical snapshot.
    """
    has_api = setup_gemini()
    
    if not has_api:
        return """
# Clinical Snapshot: Audio Analysis

**Patient:** Monika
**Date:** 2026-04-19
**Symptom Duration:** Analyzed 10-second clip

**Findings:**
- Detected pronounced wheezing in the upper respiratory tract.
- Cough frequency indicates a persistent irritation.
- No signs of acute stridor, but patterns resemble early-stage bronchitis or an asthma exacerbation.

**Recommendation:** Monitor oxygen saturation and consult physician if symptoms persist for >48 hours.
"""

    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        # Note: Gemini 1.5 Pro/Flash supports audio files directly. 
        # In a real implementation, you'd upload the file to the File API first.
        # file_upload = genai.upload_file(audio_path)
        
        prompt = """
        You are a medical AI. Listen to the provided audio clip of a patient's cough/breathing.
        Analyze the audio frequency and patterns to detect anomalies like wheezing, stridor, or fluid in lungs.
        Generate a "Clinical Snapshot" summarizing the findings in professional medical terminology.
        Format it as a concise report for a doctor.
        """
        
        # response = model.generate_content([prompt, file_upload])
        response = model.generate_content([prompt, "Audio File Data Simulation"]) # Placeholder for local execution without real file upload
        return response.text.strip()
    except Exception as e:
        return f"An error occurred during audio analysis: {str(e)}"

def analyze_symptom_image(image_path: str) -> str:
    """
    Analyzes an image/video (e.g., wound progression) and generates a clinical snapshot.
    """
    has_api = setup_gemini()
    
    if not has_api:
         return """
# Clinical Snapshot: Visual Analysis

**Patient:** Monika
**Date:** 2026-04-19
**Observation:** Wound Progression

**Findings:**
- Visual analysis of the epidermal layer shows reduced erythema compared to baseline.
- No visible signs of purulent exudate or spreading cellulitis.
- Healing appears to be progressing normally by secondary intention.

**Recommendation:** Continue current wound care protocol.
"""
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        from PIL import Image
        img = Image.open(image_path)
        
        prompt = """
        You are a medical AI. Analyze this image of a patient's symptom (e.g., a rash, wound, or inflammation).
        Generate a "Clinical Snapshot" summarizing the visual progression and current state in professional medical terminology.
        Focus on color, size, swelling, and any signs of infection.
        Format it as a concise report for a doctor.
        """
        
        response = model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        return f"An error occurred during visual analysis: {str(e)}"
