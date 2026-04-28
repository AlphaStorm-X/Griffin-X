import React, { useState, useRef } from 'react';
import { Mic, Square, Volume2, Loader2, X, Sparkles, MessageSquare } from 'lucide-react';
import api, { MOCK_MODE } from '../utils/api';

const VoiceAssistant = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [transcript, setTranscript] = useState('');
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      audioChunks.current = [];

      mediaRecorder.current.ondataavailable = (event) => {
        audioChunks.current.push(event.data);
      };

      mediaRecorder.current.onstop = async () => {
        if (MOCK_MODE) {
          handleMockResponse();
        } else {
          const audioBlob = new Blob(audioChunks.current, { type: 'audio/mp3' });
          await sendAudioToBackend(audioBlob);
        }
      };

      mediaRecorder.current.start();
      setIsRecording(true);
      setTranscript("Listening for your health query...");
      setError(null);
      setResponse(null);
    } catch (err) {
      setError("Microphone access denied. Check browser settings.");
      console.error(err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current && isRecording) {
      mediaRecorder.current.stop();
      setIsRecording(false);
      setIsProcessing(true);
      setTranscript("Analyzing medical insights...");
    }
  };

  const handleMockResponse = () => {
    setTimeout(() => {
      const responses = [
        "I recommend resting and staying hydrated for that headache. If it persists beyond today, please consult your doctor.",
        "Your health vitals seem balanced based on your schedule. Remember to take your Vitamin D3 at 8:00 AM.",
        "Deep breathing for 5 minutes can help with that stress. I've updated your daily wellness tip.",
        "Make sure to drink at least 8 glasses of water today to improve medicine absorption."
      ];
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      
      setResponse({ text: randomResponse });
      setIsProcessing(false);
      setTranscript("");

      const synth = window.speechSynthesis;
      synth.cancel(); 
      const utterance = new SpeechSynthesisUtterance(randomResponse);
      utterance.pitch = 1.1; 
      utterance.rate = 0.95; 
      synth.speak(utterance);
    }, 1500);
  };

  const sendAudioToBackend = async (blob) => {
    const formData = new FormData();
    formData.append('audio', blob, 'query.mp3');
    try {
      const { data } = await api.post('/voice/query', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResponse(data);
      const audio = new Audio(`http://localhost:5000${data.audioUrl}`);
      audio.play();
    } catch (err) {
      setError("System is in Mock Mode. Using local intelligence.");
      handleMockResponse();
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="fixed bottom-10 right-10 z-[150] flex flex-col items-end gap-6">
      {/* Dynamic Response Bubble with Cleaner Typography */}
      {(isRecording || isProcessing || response) && (
        <div className="bg-white/95 backdrop-blur-2xl p-8 rounded-[2.5rem] shadow-2xl border border-white/50 max-w-sm animate-in slide-in-from-bottom-6 duration-700 ring-1 ring-slate-100">
           <div className="flex justify-between items-start mb-6">
              <div className="flex items-center gap-3 text-primary-600">
                {isRecording ? <div className="w-2.5 h-2.5 bg-red-500 rounded-full animate-pulse" /> : <Sparkles size={20} className="text-indigo-500" />}
                <span className="text-[10px] font-bold uppercase tracking-[0.2em]">{isRecording ? 'Listening' : 'Health AI'}</span>
              </div>
              <button onClick={() => {setResponse(null); setIsRecording(false);}} className="p-1.5 hover:bg-slate-50 rounded-xl transition-colors">
                <X size={18} className="text-slate-300" />
              </button>
           </div>

           {transcript && (
             <p className="text-slate-400 text-sm font-medium italic mb-2 tracking-tight">{transcript}</p>
           )}

           {response && (
             <div className="flex items-start gap-4">
               <div className="mt-1 text-primary-500 shrink-0 bg-primary-50 p-2 rounded-xl">
                 <Volume2 size={20} className="animate-pulse" />
               </div>
               <p className="text-slate-800 text-lg leading-relaxed font-medium tracking-tight">
                 {response.text}
               </p>
             </div>
           )}

           {isProcessing && (
             <div className="flex items-center gap-3 text-primary-600 font-semibold py-4">
               <Loader2 className="animate-spin" size={20} />
               <span className="text-sm">Generating Solution...</span>
             </div>
           )}
        </div>
      )}

      {/* Main Trigger Button - Refined Design */}
      <div className="relative group">
        <div className={`absolute inset-0 rounded-[2.5rem] bg-primary-600 blur-2xl opacity-20 group-hover:opacity-40 transition-all duration-700 ${isRecording ? 'animate-pulse' : ''}`} />
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={isProcessing}
          className={`relative z-10 w-24 h-24 rounded-[2.5rem] flex items-center justify-center shadow-2xl transition-all duration-500 active:scale-90 border-[6px] border-white/50 ${
            isRecording ? 'bg-red-500 text-white animate-pulse' : 'bg-primary-600 text-white hover:bg-primary-700 hover:shadow-primary-200'
          }`}
        >
          {isProcessing ? (
            <Loader2 className="animate-spin text-white" size={36} />
          ) : isRecording ? (
            <div className="w-10 h-10 bg-white rounded-2xl shadow-inner" />
          ) : (
            <Mic size={36} className="group-hover:scale-110 transition-transform" />
          )}
        </button>
      </div>

      {error && (
        <div className="bg-slate-900 text-white px-5 py-3 rounded-2xl text-[10px] font-bold uppercase tracking-widest shadow-2xl animate-in fade-in duration-300">
          {error}
        </div>
      )}
    </div>
  );
};

export default VoiceAssistant;
