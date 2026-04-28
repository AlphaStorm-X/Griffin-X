# AURACARE/ai-layer/emergency_ai.py
"""
Emergency Detection AI Module.
Detects emergencies from video frames, audio, or text input.
"""
import json
import base64
from typing import Dict, Any, Optional
from gemini_config import get_vision_model, get_model
from prompts import EMERGENCY_SYSTEM_PROMPT, EMERGENCY_USER_PROMPT_TEMPLATE


class EmergencyDetector:
    """Handles emergency detection using Gemini AI."""

    def __init__(self):
        """Initialize the emergency detector with Gemini model."""
        self.vision_model = get_vision_model()
        self.text_model = get_model()
        self.default_response = {
            "event": "No emergency detected",
            "risk": "Low",
            "confidence": "High",
            "action": "Continue monitoring",
            "message": "No immediate emergency detected"
        }

    def _encode_image(self, image_data: bytes) -> str:
        """Encode image bytes to base64 string."""
        return base64.b64encode(image_data).decode('utf-8')

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
            required_fields = ["event", "risk",
                               "confidence", "action", "message"]
            for field in required_fields:
                if field not in result:
                    result[field] = self.default_response.get(field, "")

            # Validate risk values
            valid_risk = ["Low", "Medium", "High"]
            if result["risk"] not in valid_risk:
                result["risk"] = "Low"

            # Validate confidence values
            valid_confidences = ["High", "Medium", "Low"]
            if result["confidence"] not in valid_confidences:
                result["confidence"] = "Low"

            # Add urgency flag
            result["is_emergency"] = (result["risk"] == "High")

            return result

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response_text}")
            return self.default_response

    async def detect_from_video_frame(self, frame_bytes: bytes, previous_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Detect emergencies from video frame.

        Args:
            frame_bytes: Raw image bytes from video frame
            previous_context: Context from previous frames

        Returns:
            Dictionary with emergency detection results
        """
        try:
            # Prepare image for Gemini
            image_data = {
                "mime_type": "image/jpeg",
                "data": self._encode_image(frame_bytes)
            }

            # Prepare user prompt
            user_prompt = EMERGENCY_USER_PROMPT_TEMPLATE.format(
                input_type="video frame",
                emergency_input="Analyze this video frame for falls, distress, or emergency situations"
            )

            if previous_context:
                user_prompt += f"\n\nPrevious context: {previous_context}"

            # Generate response from Gemini vision model
            response = self.vision_model.generate_content(
                contents=[
                    EMERGENCY_SYSTEM_PROMPT,
                    user_prompt,
                    image_data
                ]
            )

            # Parse and return JSON response
            result = self._parse_json_response(response.text)

            # Add metadata
            result["_metadata"] = {
                "model": "gemini-1.5-flash",
                "timestamp": "auto-generated-by-system",
                "input_type": "video_frame"
            }

            return result

        except Exception as e:
            print(f"Emergency detection error: {e}")
            error_response = self.default_response.copy()
            error_response["message"] = f"Detection error: {str(e)}"
            return error_response

    async def detect_from_audio_transcript(self, transcript: str) -> Dict[str, Any]:
        """
        Detect emergencies from audio transcript.

        Args:
            transcript: Transcribed audio text

        Returns:
            Dictionary with emergency detection results
        """
        try:
            # Prepare user prompt
            user_prompt = EMERGENCY_USER_PROMPT_TEMPLATE.format(
                input_type="audio transcript",
                emergency_input=transcript
            )

            # Generate response from Gemini text model
            response = self.text_model.generate_content(
                contents=[
                    EMERGENCY_SYSTEM_PROMPT,
                    user_prompt
                ]
            )

            # Parse and return JSON response
            result = self._parse_json_response(response.text)

            # Add metadata
            result["_metadata"] = {
                "model": "gemini-1.5-flash",
                "timestamp": "auto-generated-by-system",
                "input_type": "audio_transcript"
            }

            return result

        except Exception as e:
            print(f"Emergency detection error: {e}")
            error_response = self.default_response.copy()
            error_response["message"] = f"Detection error: {str(e)}"
            return error_response

    def detect_from_video_sync(self, frame_path: str, previous_context: Optional[str] = None) -> Dict[str, Any]:
        """
        Synchronous wrapper for video frame detection.

        Args:
            frame_path: Path to video frame image
            previous_context: Optional context from previous frames

        Returns:
            Dictionary with emergency detection results
        """
        import asyncio

        # Read image file
        with open(frame_path, 'rb') as f:
            frame_bytes = f.read()

        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            self.detect_from_video_frame(frame_bytes, previous_context))
        loop.close()

        return result

    def detect_from_audio_sync(self, transcript: str) -> Dict[str, Any]:
        """
        Synchronous wrapper for audio transcript detection.

        Args:
            transcript: Transcribed audio text

        Returns:
            Dictionary with emergency detection results
        """
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            self.detect_from_audio_transcript(transcript))
        loop.close()

        return result


# Singleton instance for easy import
emergency_detector = EmergencyDetector()


# Convenience functions
def detect_emergency_from_video(frame_path: str) -> Dict[str, Any]:
    """Quick function to detect emergency from video frame."""
    return emergency_detector.detect_from_video_sync(frame_path)


def detect_emergency_from_audio(transcript: str) -> Dict[str, Any]:
    """Quick function to detect emergency from audio transcript."""
    return emergency_detector.detect_from_audio_sync(transcript)
