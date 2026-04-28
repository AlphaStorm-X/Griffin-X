# AURACARE/ai-layer/digital_twin.py
"""
Digital Twin AI Module.
Creates and maintains patient health profiles for personalized care.
"""
import json
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
from gemini_config import get_model
from prompts import DIGITAL_TWIN_SYSTEM_PROMPT, DIGITAL_TWIN_USER_PROMPT_TEMPLATE


class DigitalTwin:
    """Manages patient digital twin health profiles."""

    def __init__(self):
        """Initialize digital twin with Gemini model."""
        self.model = get_model()
        self.profiles = {}  # In-memory storage (replace with DB in production)
        self.default_response = {
            "profile_id": "",
            "baseline_health": {
                "key_metrics": [],
                "risk_factors": []
            },
            "recommendations": {
                "immediate": ["Consult healthcare provider"],
                "long_term": ["Regular health checkups"]
            },
            "alert_triggers": ["Any sudden change in symptoms"],
            "summary": "Patient profile created"
        }

    def _parse_json_response(self, response_text: str, profile_id: str) -> Dict[str, Any]:
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

            # Add profile_id if missing
            if "profile_id" not in result or not result["profile_id"]:
                result["profile_id"] = profile_id

            # Ensure required structure
            if "baseline_health" not in result:
                result["baseline_health"] = self.default_response["baseline_health"]
            if "recommendations" not in result:
                result["recommendations"] = self.default_response["recommendations"]
            if "alert_triggers" not in result:
                result["alert_triggers"] = self.default_response["alert_triggers"]
            if "summary" not in result:
                result["summary"] = self.default_response["summary"]

            return result

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            error_response = self.default_response.copy()
            error_response["profile_id"] = profile_id
            return error_response

    async def create_profile(self, medical_history: str, recent_symptoms: str,
                             medications: str, vitals: str) -> Dict[str, Any]:
        """
        Create a new digital twin health profile.

        Args:
            medical_history: Patient's medical history
            recent_symptoms: Recent symptoms experienced
            medications: Current medications
            vitals: Vital signs data

        Returns:
            Dictionary with digital twin profile
        """
        try:
            # Generate unique profile ID
            profile_id = str(uuid.uuid4())

            # Prepare user prompt
            user_prompt = DIGITAL_TWIN_USER_PROMPT_TEMPLATE.format(
                medical_history=medical_history or "None provided",
                recent_symptoms=recent_symptoms or "None provided",
                medications=medications or "None provided",
                vitals=vitals or "None provided"
            )

            # Generate response from Gemini
            response = self.model.generate_content(
                contents=[
                    DIGITAL_TWIN_SYSTEM_PROMPT,
                    user_prompt
                ]
            )

            # Parse and return JSON response
            result = self._parse_json_response(response.text, profile_id)

            # Add metadata
            result["_metadata"] = {
                "model": "gemini-1.5-flash",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0"
            }

            # Store profile
            self.profiles[profile_id] = result

            return result

        except Exception as e:
            print(f"Digital twin creation error: {e}")
            error_response = self.default_response.copy()
            error_response["profile_id"] = str(uuid.uuid4())
            error_response["summary"] = f"Profile creation error: {str(e)}"
            return error_response

    async def update_profile(self, profile_id: str, new_symptoms: str,
                             new_vitals: Optional[str] = None) -> Dict[str, Any]:
        """
        Update existing digital twin profile with new data.

        Args:
            profile_id: Existing profile ID
            new_symptoms: New symptoms to add
            new_vitals: Updated vital signs

        Returns:
            Updated profile
        """
        try:
            # Get existing profile
            existing_profile = self.profiles.get(profile_id)
            if not existing_profile:
                raise ValueError(f"Profile {profile_id} not found")

            # Combine with new data
            update_prompt = f"""
            Update the existing health profile with new information.
            
            Existing profile summary: {existing_profile.get('summary', 'No summary')}
            New symptoms: {new_symptoms}
            New vitals: {new_vitals or 'Not provided'}
            
            Provide updated JSON profile maintaining the same structure.
            """

            # Generate updated profile
            response = self.model.generate_content(
                contents=[
                    DIGITAL_TWIN_SYSTEM_PROMPT,
                    update_prompt
                ]
            )

            # Parse response
            result = self._parse_json_response(response.text, profile_id)

            # Preserve profile_id and update metadata
            result["profile_id"] = profile_id
            result["_metadata"] = {
                "model": "gemini-1.5-flash",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "updated_from": existing_profile.get("_metadata", {}).get("timestamp")
            }

            # Update stored profile
            self.profiles[profile_id] = result

            return result

        except Exception as e:
            print(f"Digital twin update error: {e}")
            return {
                "profile_id": profile_id,
                "error": str(e),
                "summary": "Profile update failed"
            }

    def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a digital twin profile."""
        return self.profiles.get(profile_id)

    def create_profile_sync(self, medical_history: str, recent_symptoms: str,
                            medications: str, vitals: str) -> Dict[str, Any]:
        """Synchronous wrapper for profile creation."""
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.create_profile(
            medical_history, recent_symptoms, medications, vitals
        ))
        loop.close()

        return result


# Singleton instance
digital_twin = DigitalTwin()


# Convenience function
def create_health_profile(medical_history: str = "", recent_symptoms: str = "",
                          medications: str = "", vitals: str = "") -> Dict[str, Any]:
    """Quick function to create a health profile."""
    return digital_twin.create_profile_sync(
        medical_history, recent_symptoms, medications, vitals
    )
