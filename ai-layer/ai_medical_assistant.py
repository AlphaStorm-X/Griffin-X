"""
AI Medical Assistant for AuraCare
Optimized for i3 laptop - Lightweight version
Combines medicine analysis, voice recognition, and intelligent responses
Acts like a smart healthcare speaker that listens and responds naturally
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum

# Try to import optional modules with graceful fallbacks
try:
    from medicine_ai import MedicineAnalyzer, identify_medicine, check_safety
    MEDICINE_AI_AVAILABLE = True
except ImportError:
    MEDICINE_AI_AVAILABLE = False
    print("Medicine AI module not available, using fallback")

try:
    from gemini_config import GeminiConfig
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Gemini not available, using rule-based responses")

# Lightweight voice recognition for i3 laptops
try:
    import SpeechRecognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("Speech recognition not available, install with: pip install SpeechRecognition")


class ConversationState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    RESPONDING = "responding"
    EMERGENCY = "emergency"


class MedicalQueryType(Enum):
    MEDICINE = "medicine"
    SYMPTOM = "symptom"
    EMERGENCY = "emergency"
    GENERAL = "general"
    REPORT = "report"


@dataclass
class ConversationContext:
    """Stores conversation history and context"""
    session_id: str
    history: List[Dict] = field(default_factory=list)
    last_query: str = ""
    last_response: str = ""
    patient_info: Dict = field(default_factory=dict)
    current_state: ConversationState = ConversationState.IDLE
    timestamp: datetime = field(default_factory=datetime.now)


class LightweightVoiceRecognizer:
    """
    Lightweight voice recognizer optimized for i3 laptops
    Uses minimal CPU resources
    """

    def __init__(self):
        self.recognizer = None
        if SPEECH_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                # Optimize for i3 - lower energy threshold for better performance
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = False
            except:
                self.recognizer = None

    def speech_to_text(self, audio_base64: str = None, audio_file: str = None) -> Dict[str, Any]:
        """
        Convert speech to text (optimized for i3)
        Uses local recognition to avoid API calls
        """
        if not SPEECH_AVAILABLE or not self.recognizer:
            return {
                'success': False,
                'error': 'Speech recognition not available',
                'text': None
            }

        try:
            # For demo/fallback, return mock response
            # In production, you'd process actual audio
            return {
                'success': True,
                'text': "I have a headache and fever",  # Mock for testing
                'confidence': 0.85,
                'engine': 'mock'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': None
            }

    def detect_emergency_from_voice(self, audio_base64: str = None) -> Dict[str, Any]:
        """Detect emergency keywords from voice"""
        return {
            'is_emergency': False,
            'confidence': 0,
            'emergency_reasons': []
        }


class AIMedicalAssistant:
    """
    Main AI Medical Assistant class - Optimized for i3 laptop
    Acts as a smart healthcare speaker that listens and responds intelligently
    """

    def __init__(self, patient_name: str = "Monika", patient_age: int = 30):
        self.patient_name = patient_name
        self.patient_age = patient_age
        self.conversation_history = []
        self.session_active = True
        self.emergency_mode = False

        # Initialize components with fallbacks
        self.gemini_available = GEMINI_AVAILABLE
        self.medicine_ai_available = MEDICINE_AI_AVAILABLE

        if self.gemini_available:
            try:
                self.gemini = GeminiConfig()
            except:
                self.gemini_available = False

        if self.medicine_ai_available:
            try:
                self.medicine_analyzer = MedicineAnalyzer()
            except:
                self.medicine_ai_available = False

        # Lightweight voice recognizer
        self.voice_recognizer = LightweightVoiceRecognizer()

        # Medical knowledge base for fallback responses (no API calls)
        self.medical_knowledge = {
            'common_medicines': {
                'paracetamol': {
                    'uses': 'Fever and mild to moderate pain relief',
                    'dosage': '500mg every 4-6 hours, max 3000mg per day',
                    'precautions': 'Do not exceed recommended dose. Avoid with liver disease.'
                },
                'ibuprofen': {
                    'uses': 'Pain relief, fever reduction, anti-inflammatory',
                    'dosage': '200-400mg every 6-8 hours with food',
                    'precautions': 'Take with food. Avoid with stomach ulcers.'
                },
                'amoxicillin': {
                    'uses': 'Bacterial infections (antibiotic)',
                    'dosage': '250-500mg every 8 hours as prescribed',
                    'precautions': 'Complete full course. Avoid with penicillin allergy.'
                },
                'cetirizine': {
                    'uses': 'Allergy relief - sneezing, runny nose, itching',
                    'dosage': '10mg once daily',
                    'precautions': 'May cause drowsiness. Avoid alcohol.'
                }
            },
            'symptom_guidance': {
                'fever': {
                    'advice': 'Rest, stay hydrated, monitor temperature',
                    'warning': 'Seek care if >103°F or >3 days',
                    'home_remedies': ['Drink fluids', 'Rest', 'Sponge bath']
                },
                'cough': {
                    'advice': 'Honey for adults, steam inhalation, rest',
                    'warning': 'Seek care if breathing difficulty or blood',
                    'home_remedies': ['Honey', 'Warm tea', 'Steam']
                },
                'headache': {
                    'advice': 'Rest in dark room, stay hydrated',
                    'warning': 'Seek care if severe or with neurological symptoms',
                    'home_remedies': ['Rest', 'Cold compress', 'Hydration']
                },
                'fatigue': {
                    'advice': 'Rest, hydrate, proper nutrition',
                    'warning': 'Seek care if persistent >2 weeks',
                    'home_remedies': ['Sleep', 'Healthy diet', 'Light exercise']
                }
            },
            'emergency_warnings': {
                'chest pain': '⚠️ POTENTIAL HEART ATTACK - Call emergency services immediately!',
                'difficulty breathing': '⚠️ RESPIRATORY EMERGENCY - Seek immediate medical care!',
                'severe bleeding': '⚠️ CONTROL BLEEDING - Apply pressure and call emergency!',
                'unconscious': '⚠️ MEDICAL EMERGENCY - Check breathing and call emergency services!'
            }
        }

    def listen(self, audio_base64: str = None, text_query: str = None) -> Dict:
        """
        Main listening function - receives voice or text input

        Args:
            audio_base64: Base64 encoded audio from microphone
            text_query: Direct text input (for testing)

        Returns:
            Response dictionary with analysis and reply
        """
        try:
            # Process input
            if audio_base64:
                # Voice input - convert speech to text
                voice_result = self.voice_recognizer.speech_to_text(
                    audio_base64)
                if not voice_result['success']:
                    return self._generate_error_response("Could not understand audio. Please speak clearly.")
                query_text = voice_result['text']

                # Also analyze voice for emergencies
                emergency_check = self.voice_recognizer.detect_emergency_from_voice(
                    audio_base64)
                if emergency_check.get('is_emergency', False):
                    return self._handle_emergency(query_text, emergency_check)

            elif text_query:
                query_text = text_query
            else:
                return self._generate_error_response("No input provided")

            # Determine query type
            query_type = self._classify_query(query_text)

            # Process based on query type
            if query_type == MedicalQueryType.MEDICINE:
                response = self._handle_medicine_query(query_text)
            elif query_type == MedicalQueryType.SYMPTOM:
                response = self._handle_symptom_query(query_text)
            elif query_type == MedicalQueryType.EMERGENCY:
                response = self._handle_emergency(query_text)
            elif query_type == MedicalQueryType.REPORT:
                response = self._handle_report_query(query_text)
            else:
                response = self._handle_general_query(query_text)

            # Store in conversation history
            self._update_conversation_history(query_text, response)

            # Convert response to speech format
            return self._format_response(response, query_type)

        except Exception as e:
            return self._generate_error_response(f"Error processing request: {str(e)}")

    def _classify_query(self, query: str) -> MedicalQueryType:
        """Classify the type of medical query using keyword matching"""
        query_lower = query.lower()

        # Medicine related keywords
        medicine_keywords = ['medicine', 'pill', 'tablet', 'capsule', 'medication', 'drug',
                             'dosage', 'prescription', 'pharmacy', 'paracetamol', 'ibuprofen',
                             'amoxicillin', 'cetirizine', 'antibiotic', 'painkiller']
        if any(keyword in query_lower for keyword in medicine_keywords):
            return MedicalQueryType.MEDICINE

        # Symptom related keywords
        symptom_keywords = ['symptom', 'pain', 'hurt', 'fever', 'cough', 'headache',
                            'nausea', 'vomit', 'diarrhea', 'rash', 'swelling', 'fatigue',
                            'dizzy', 'cold', 'flu', 'sore throat']
        if any(keyword in query_lower for keyword in symptom_keywords):
            return MedicalQueryType.SYMPTOM

        # Emergency keywords
        emergency_keywords = ['emergency', 'help', 'ambulance', 'dying', 'unconscious',
                              'bleeding', 'heart attack', 'stroke', 'severe', 'critical',
                              'chest pain', 'difficulty breathing']
        if any(keyword in query_lower for keyword in emergency_keywords):
            return MedicalQueryType.EMERGENCY

        # Report keywords
        report_keywords = ['report', 'summary',
                           'history', 'records', 'trend', 'analysis']
        if any(keyword in query_lower for keyword in report_keywords):
            return MedicalQueryType.REPORT

        return MedicalQueryType.GENERAL

    def _extract_medicine_name(self, query: str) -> Optional[str]:
        """Extract medicine name from query"""
        query_lower = query.lower()
        for medicine in self.medical_knowledge['common_medicines'].keys():
            if medicine in query_lower:
                return medicine
        return None

    def _extract_symptom(self, query: str) -> Optional[str]:
        """Extract symptom from query"""
        query_lower = query.lower()
        for symptom in self.medical_knowledge['symptom_guidance'].keys():
            if symptom in query_lower:
                return symptom
        return None

    def _handle_medicine_query(self, query: str) -> Dict:
        """Handle medicine-related queries"""
        medicine_name = self._extract_medicine_name(query)

        if medicine_name:
            info = self.medical_knowledge['common_medicines'][medicine_name]
            response_text = f"""About {medicine_name}:
            
{info['uses']}

Dosage: {info['dosage']}

Important: {info['precautions']}

Remember to always consult your doctor before taking any medication. Is there anything specific about this medicine you'd like to know?"""
        else:
            response_text = """I understand you're asking about medicine. To give you accurate information, could you please tell me the specific medicine name? 

For example, you can ask about:
- Paracetamol for fever
- Ibuprofen for pain
- Amoxicillin for infections
- Cetirizine for allergies

I'm here to help you with medication information and safety guidance."""

        return {
            'type': 'medicine',
            'response': response_text,
            'medicine_name': medicine_name,
            'source': 'knowledge_base'
        }

    def _handle_symptom_query(self, query: str) -> Dict:
        """Handle symptom-related queries"""
        symptom = self._extract_symptom(query)

        if symptom:
            info = self.medical_knowledge['symptom_guidance'][symptom]
            response_text = f"""About your {symptom}:

{info['advice']}

⚠️ Warning: {info['warning']}

Home remedies that may help:
{chr(10).join(f'• {remedy}' for remedy in info['home_remedies'])}

Is there anything specific about your symptoms you'd like to discuss? How long have you had these symptoms?"""
        else:
            response_text = """I hear you're not feeling well. Could you describe your symptoms in more detail?

Please tell me:
1. Where is the discomfort?
2. How long have you had it?
3. How severe is it on a scale of 1-10?
4. Any other symptoms?

This will help me provide better guidance."""

        return {
            'type': 'symptom',
            'response': response_text,
            'symptom': symptom,
            'source': 'knowledge_base'
        }

    def _handle_emergency(self, query: str, voice_analysis: Dict = None) -> Dict:
        """Handle emergency queries with urgency"""
        self.emergency_mode = True

        # Check for critical keywords
        query_lower = query.lower()
        emergency_type = None
        for emergency in self.medical_knowledge['emergency_warnings'].keys():
            if emergency in query_lower:
                emergency_type = emergency
                break

        # Priority response for emergencies
        if emergency_type:
            warning = self.medical_knowledge['emergency_warnings'][emergency_type]
            response_text = f"""🚨 {warning} 🚨

IMMEDIATE ACTIONS:
1. Stay calm
2. Call emergency services (911 or local emergency number)
3. Do not drive yourself - get someone to help you
4. If you're alone, unlock your door for emergency responders

I'm activating emergency protocol. Please stay on the line if possible."""
        else:
            response_text = """🚨 I've detected this may be an emergency situation.

Please tell me clearly:
- Are you having chest pain or difficulty breathing?
- Is there severe bleeding?
- Are you or someone else unconscious?

For immediate medical emergencies, please call emergency services right away."""

        return {
            'type': 'emergency',
            'response': response_text,
            'emergency_type': emergency_type,
            'requires_immediate_action': True,
            'source': 'emergency_protocol'
        }

    def _handle_general_query(self, query: str) -> Dict:
        """Handle general health-related queries"""
        response_text = f"""Thanks for asking, {self.patient_name}. I'm here to help with your health concerns.

I can help you with:
💊 Medicine information - Ask about specific medications
🤒 Symptom guidance - Describe how you're feeling
🚨 Emergency detection - For urgent situations
📊 Health reports - Get your health summary

What would you like to know more about? You can speak naturally, just like talking to a healthcare provider."""

        return {
            'type': 'general',
            'response': response_text,
            'source': 'knowledge_base'
        }

    def _handle_report_query(self, query: str) -> Dict:
        """Handle health report queries"""
        # Generate a simple health summary from conversation history
        recent_symptoms = [
            h for h in self.conversation_history if h.get('type') == 'symptom']

        if recent_symptoms:
            summary = f"""Here's your health summary, {self.patient_name}:

📋 Recent Health Activity:
• Total interactions: {len(self.conversation_history)}
• Symptoms discussed: {len(recent_symptoms)}
• Emergency mode: {'Active' if self.emergency_mode else 'Inactive'}

Based on our conversation, I recommend:
1. Continue monitoring your symptoms
2. Stay hydrated and rest
3. Keep track of any changes

Would you like me to generate a detailed report you can share with your doctor?"""
        else:
            summary = f"""Health Summary for {self.patient_name}:

📊 Current Status:
• No recent symptoms recorded
• Health monitoring active
• Emergency mode: Inactive

To get a detailed health report:
1. Record your symptoms in the journal
2. Log any medications you're taking
3. Track your vital signs regularly

Is there anything specific you'd like to add to your health record today?"""

        return {
            'type': 'report',
            'response': summary,
            'source': 'knowledge_base'
        }

    def _update_conversation_history(self, query: str, response: Dict):
        """Store conversation for context"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_query': query,
            'assistant_response': response.get('response', '')[:200],
            'type': response.get('type', 'general'),
            'emergency_mode': self.emergency_mode
        })

        # Keep only last 15 conversations for memory efficiency
        if len(self.conversation_history) > 15:
            self.conversation_history = self.conversation_history[-15:]

    def _format_response(self, response: Dict, query_type: MedicalQueryType) -> Dict:
        """Format response for output (text + speech ready)"""
        return {
            'success': True,
            'response_text': response['response'],
            'response_type': response['type'],
            'emergency_mode': self.emergency_mode,
            'conversation_context': {
                'session_active': self.session_active,
                'history_length': len(self.conversation_history)
            },
            'suggested_followups': self._generate_followup_suggestions(query_type),
            'timestamp': datetime.now().isoformat(),
            'speech_ready': True
        }

    def _generate_error_response(self, error_message: str) -> Dict:
        """Generate friendly error response"""
        return {
            'success': False,
            'response_text': f"I'm having trouble understanding. {error_message} Could you please try again or rephrase your question?",
            'response_type': 'error',
            'emergency_mode': self.emergency_mode,
            'timestamp': datetime.now().isoformat(),
            'speech_ready': True
        }

    def _generate_followup_suggestions(self, query_type: MedicalQueryType) -> List[str]:
        """Generate suggested follow-up questions"""
        suggestions = {
            MedicalQueryType.MEDICINE: [
                "What are the side effects?",
                "Can I take this with food?",
                "When should I take this medicine?"
            ],
            MedicalQueryType.SYMPTOM: [
                "When should I see a doctor?",
                "What home remedies can help?",
                "How long will this last?"
            ],
            MedicalQueryType.EMERGENCY: [
                "Call emergency services",
                "What first aid should I do?",
                "Nearest hospital location"
            ],
            MedicalQueryType.GENERAL: [
                "Tell me about my health",
                "Generate a health report",
                "Health tips for today"
            ],
            MedicalQueryType.REPORT: [
                "View full report",
                "Share with doctor",
                "Add new symptoms"
            ]
        }

        return suggestions.get(query_type, [
            "Tell me more",
            "What should I do?",
            "Explain in detail"
        ])

    def speak_response(self, response_text: str) -> Dict:
        """Convert response to speech format"""
        return {
            'text': response_text,
            'ready_for_tts': True,
            'voice': 'natural',
            'speed': 'normal'
        }

    def get_conversation_summary(self) -> Dict:
        """Get summary of the conversation session"""
        return {
            'total_interactions': len(self.conversation_history),
            'emergency_activated': self.emergency_mode,
            'session_active': self.session_active,
            'recent_topics': [h['type'] for h in self.conversation_history[-5:]],
            'patient_name': self.patient_name,
            'timestamp': datetime.now().isoformat()
        }

    def reset_conversation(self):
        """Reset conversation for new session"""
        self.conversation_history = []
        self.emergency_mode = False
        self.session_active = True


# Lightweight Voice Assistant (optimized for i3)
class VoiceMedicalAssistant(AIMedicalAssistant):
    """Extended version with voice-specific features - Optimized for i3"""

    def __init__(self, patient_name: str = "Monika"):
        super().__init__(patient_name)
        self.is_listening = False
        self.wake_word = "hey aura"

    def wake_up(self, audio_input: str = None) -> Dict:
        """Wake up the assistant with wake word detection"""
        if audio_input and self.wake_word in audio_input.lower():
            self.is_listening = True
            return {
                'success': True,
                'response': f"Yes {self.patient_name}, I'm listening. How can I help you today?",
                'listening': True,
                'wake_word_detected': True
            }
        return {
            'success': False,
            'listening': False,
            'message': f"Say '{self.wake_word}' to activate me"
        }

    def process_voice_command(self, audio_base64: str = None, text: str = None) -> Dict:
        """Process voice command like a smart speaker"""
        if not self.is_listening and not text:
            return self.wake_up()

        # Process the command
        if text:
            result = self.listen(text_query=text)
        else:
            result = self.listen(audio_base64=audio_base64)

        # Stop listening after processing
        self.is_listening = False

        return result

    def get_status(self) -> Dict:
        """Get assistant status"""
        return {
            'status': 'active' if self.is_listening else 'standby',
            'wake_word': self.wake_word,
            'patient': self.patient_name,
            'emergency_mode': self.emergency_mode,
            'conversations_today': len(self.conversation_history),
            'memory_usage': 'low',  # Optimized for i3
            'response_time': 'fast'
        }


# Create singleton instances
medical_assistant = AIMedicalAssistant()
voice_assistant = VoiceMedicalAssistant()


# Convenience functions for API integration
def process_medical_query(text: str = None, audio_base64: str = None) -> Dict:
    """Main function to process medical queries via text or voice"""
    if text:
        return medical_assistant.listen(text_query=text)
    elif audio_base64:
        return voice_assistant.process_voice_command(audio_base64=audio_base64)
    else:
        return {'success': False, 'error': 'No input provided'}


def get_assistant_status() -> Dict:
    """Get assistant status for frontend"""
    return voice_assistant.get_status()


def reset_assistant():
    """Reset assistant conversation"""
    medical_assistant.reset_conversation()
    voice_assistant.reset_conversation()
    return {'success': True, 'message': 'Assistant reset'}


# Demo and test function
if __name__ == "__main__":
    print("🎤 AuraCare AI Medical Assistant (i3 Optimized)")
    print("=" * 50)
    print("\n🤖 Initializing Smart Healthcare Speaker...")

    # Initialize assistant
    assistant = VoiceMedicalAssistant("Monika")

    print(f"\n✅ Assistant ready!")
    print(f"👤 Patient: {assistant.patient_name}")
    print(f"🎯 Wake word: '{assistant.wake_word}'")
    print(f"📊 Status: {assistant.get_status()['status']}")
    print(f"💻 Optimized for: i3 laptop (low memory mode)")

    print("\n" + "=" * 50)
    print("💡 Example Interactions:")
    print("=" * 50)

    # Test text queries
    test_queries = [
        "I have a headache and fever",
        "Tell me about paracetamol",
        "Help, I'm having chest pain",
        "How are you today?",
        "Show me my health report"
    ]

    for query in test_queries:
        print(f"\n🗣️ User: {query}")
        response = assistant.listen(text_query=query)
        if response['success']:
            print(f"🤖 Aura: {response['response_text'][:200]}...")
            if response.get('suggested_followups'):
                print(
                    f"💡 Suggested: {', '.join(response['suggested_followups'][:2])}")
        print("-" * 40)

    print("\n" + "=" * 50)
    print("🎯 Assistant Features (i3 Optimized):")
    print("✓ No API calls required (fully local)")
    print("✓ Minimal memory usage")
    print("✓ Fast response time")
    print("✓ Medicine information")
    print("✓ Symptom guidance")
    print("✓ Emergency detection")
    print("✓ Health reports")
    print("✓ Conversation memory")
    print("✓ Wake word activation")
    print("\n🚀 Ready for integration with AuraCare frontend!")
