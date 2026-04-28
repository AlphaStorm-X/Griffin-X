# AURACARE/ai-layer/gemini_config.py
"""
Gemini API configuration and client setup.
Loads API key from environment variable or .env file.
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable not set. Please set it in .env file or environment.")

# Configure the Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# Model configuration
MODEL_NAME = "gemini-1.5-flash"  # Using flash for faster responses in hackathon
# For better accuracy, use "gemini-1.5-pro"

# Generation configuration
GENERATION_CONFIG = {
    "temperature": 0.2,  # Lower temperature for more consistent, deterministic outputs
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

# Safety settings - moderate for healthcare context
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]


def get_model():
    """Returns configured Gemini model instance."""
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=GENERATION_CONFIG,
        safety_settings=SAFETY_SETTINGS
    )


def get_vision_model():
    """Returns configured Gemini vision model instance."""
    # Same model - Gemini 1.5 Flash supports vision natively
    return get_model()
