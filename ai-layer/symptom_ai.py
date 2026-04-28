# AURACARE/ai-layer/symptom_ai.py
"""
Symptom Analysis AI Module.
Analyzes text or transcribed audio symptoms for assessment.
"""
from prompts import SYMPTOM_SYSTEM_PROMPT, SYMPTOM_USER_PROMPT_TEMPLATE
import json
from typing import Dict, Any, Optional
from geminiconfig.def yourFunction(x):
    return x*x

# df is your dataframe
# example function is applicable for all INT dataframe
df_squared = df.apply(yourFunction) import get_model


class SymptomAnalyzer:
    """Handles symptom analysis using Gemini AI."""

    def __init__(self):
        """Initialize the symptom analyzer with Gemini model."""
        self.model = get_model()
        self.default_response = {
            "symptom": "Unknown",
            "severity": "Mild",
            "trend": "Stable",
            "confidence": "Low",
            "advice": "Please consult a healthcare professional for proper evaluation"
        }

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response to extract JSON."""
        try:
            # Clean up response
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.startswith('```'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            # Parse JSON
            result = json.loads(cleaned)

            # Validate required fields
            required_fields = ["symptom", "severity",
                               "trend", "confidence", "advice"]
            for field in required_fields:
                if field not in result:
                    result[field] = self.default_response.get(field, "")

            # Validate severity values
            valid_severity = ["Mild", "Moderate", "Severe"]
            if result["severity"] not in valid_severity:
                result["severity"] = "Mild"

            # Validate trend values
            valid_trend = ["Improving", "Stable", "Worsening"]
            if result["trend"] not in valid_trend:
                result["trend"] = "Stable"

            # Validate confidence values
            valid_confidences = ["High", "Medium", "Low"]
            if result["confidence"] not in valid_confidences:
                result["confidence"] = "Low"

            # Add emergency flag if severity is Severe
            result["emergency_required"] = (result["severity"] == "Severe")

            return result

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response_text}")
            return self.default_response

    async def analyze_symptoms(self, symptom_text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze symptoms from text input.

        Args:
            symptom_text: Patient's symptom description
            context: Optional context (age, medical history, etc.)

        Returns:
            Dictionary with symptom analysis results
        """
        try:
            # Prepare user prompt with symptoms
            user_prompt = SYMPTOM_USER_PROMPT_TEMPLATE.format(
                symptom_input=symptom_text)

            # Add context if provided
            if context:
                context_str = "\n\nAdditional patient context:\n"
                for key, value in context.items():
                    context_str += f"- {key}: {value}\n"
                user_prompt += context_str

            # Generate response from Gemini
            response = self.model.generate_content(
                contents=[
                    SYMPTOM_SYSTEM_PROMPT,
                    user_prompt
                ]
            )

            # Parse and return JSON response
            result = self._parse_json_response(response.text)

            # Add metadata
            result["_metadata"] = {
                "model": "gemini-1.5-flash",
                "timestamp": "auto-generated-by-system",
                "input_length": len(symptom_text)
            }

            return result

        except Exception as e:
            print(f"Symptom analysis error: {e}")
            error_response = self.default_response.copy()
            error_response["advice"] = f"Analysis error: {str(e)}. Please consult a healthcare professional."
            return error_response

    def analyze_symptoms_sync(self, symptom_text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Synchronous wrapper for symptom analysis.

        Args:
            symptom_text: Patient's symptom description
            context: Optional context dictionary

        Returns:
            Dictionary with symptom analysis results
        """
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            self.analyze_symptoms(symptom_text, context))
        loop.close()

        return result


# Singleton instance for easy import
symptom_analyzer = SymptomAnalyzer()


# Convenience function
def analyze_symptoms(symptom_text: str, patient_age: Optional[int] = None,
                     medical_history: Optional[str] = None) -> Dict[str, Any]:
    """
    Quick function to analyze symptoms.

    Args:
        symptom_text: Patient's symptom description
        patient_age: Optional patient age
        medical_history: Optional medical history

    Returns:
        Symptom analysis JSON
    """
    context = {}
    if patient_age:
        context["age"] = patient_age
    if medical_history:
        context["medical_history"] = medical_history

    return symptom_analyzer.analyze_symptoms_sync(symptom_text, context if context else None)
