import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useRef,
} from "react";
import api from "../utils/api";

const AlarmContext = createContext();

export const useAlarm = () => useContext(AlarmContext);

export const AlarmProvider = ({ children }) => {
  const [activeAlarm, setActiveAlarm] = useState(null);
  const [medicines, setMedicines] = useState([]);
  const [triggeredAlarms, setTriggeredAlarms] = useState(new Set());
  const audioRef = useRef(null);

  // Initialize audio
  useEffect(() => {
    // Royalty-free alarm sound
    audioRef.current = new Audio(
      "https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3",
    );
    audioRef.current.loop = true;

    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  const fetchMedicinesFromApi = async () => {
    try {
      const { data } = await api.get("/api/medicines/today");
      setMedicines(data);
    } catch (error) {
      console.error("Error fetching medicines for alarms:", error);
    }
  };

  // Sync with API periodically
  useEffect(() => {
    fetchMedicinesFromApi();
    const interval = setInterval(fetchMedicinesFromApi, 30000); // Poll every 30 seconds
    return () => clearInterval(interval);
  }, []);

  // Monitor time for alarms
  useEffect(() => {
    const checkAlarms = () => {
      const now = new Date();
      const currentTime = `${now.getHours().toString().padStart(2, "0")}:${now.getMinutes().toString().padStart(2, "0")}`;
      const today = now.toDateString();

      medicines.forEach((med) => {
        const medId = med._id || med.id;
        // Only check if time matches, not already taken, and not already triggered this minute
        med.time.forEach((time, index) => {
          const alarmKey = `${medId}-${time}-${today}`;

          if (
            time === currentTime &&
            !med.takenStatus[index] &&
            !triggeredAlarms.has(alarmKey) &&
            !activeAlarm
          ) {
            triggerAlarm(med, index, alarmKey);
          }
        });
      });
    };

    const interval = setInterval(checkAlarms, 10000); // Check every 10 seconds
    return () => clearInterval(interval);
  }, [medicines, triggeredAlarms, activeAlarm]);

  const speakReminder = (medicine) => {
    if ("speechSynthesis" in window) {
      // Cancel any ongoing speech
      window.speechSynthesis.cancel();

      const text = `Time to take your medication: ${medicine.name}. Dosage: ${medicine.dosage}. Instruction: ${medicine.condition}.`;
      const utterance = new SpeechSynthesisUtterance(text);

      // Look for a premium-sounding voice if available
      const voices = window.speechSynthesis.getVoices();
      const preferredVoice =
        voices.find(
          (v) => v.name.includes("Google") || v.name.includes("Premium"),
        ) || voices[0];
      if (preferredVoice) utterance.voice = preferredVoice;

      utterance.rate = 0.9; // Slightly slower for clarity
      utterance.pitch = 1.0;

      window.speechSynthesis.speak(utterance);
    }
  };

  const triggerAlarm = (medicine, timeIndex, alarmKey) => {
    setActiveAlarm({ ...medicine, timeIndex });
    setTriggeredAlarms((prev) => new Set(prev).add(alarmKey));

    // Play sound (browser may block this if no user interaction yet)
    if (audioRef.current) {
      audioRef.current
        .play()
        .catch((err) =>
          console.log("Audio play blocked: awaiting user interaction", err),
        );
    }

    // Voice announcement
    speakReminder(medicine);
  };

  const stopAlarm = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    // Stop voice
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    setActiveAlarm(null);
  };

  const markAsTaken = async () => {
    if (!activeAlarm) return;
    const medId = activeAlarm._id || activeAlarm.id;

    try {
      const takenStatus = activeAlarm.takenStatus.map((s, i) =>
        i === activeAlarm.timeIndex ? true : s
      );
      await api.patch(`/api/medicines/${medId}`, { takenStatus });
      fetchMedicinesFromApi();
      stopAlarm();
    } catch (error) {
      console.error("Error marking medicine as taken from alarm:", error);
    }
  };

  const snoozeAlarm = async (minutes = 15) => {
    if (!activeAlarm) return;
    const medId = activeAlarm._id || activeAlarm.id;

    try {
      const newTimes = [...activeAlarm.time];
      const [hours, mins] = newTimes[activeAlarm.timeIndex].split(":");
      const date = new Date();
      date.setHours(parseInt(hours), parseInt(mins) + minutes);
      newTimes[activeAlarm.timeIndex] = `${date.getHours().toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}`;

      await api.patch(`/api/medicines/${medId}`, { 
        time: newTimes 
      });
      fetchMedicinesFromApi();
      stopAlarm();
    } catch (error) {
      console.error("Error snoozing alarm:", error);
    }
  };

  return (
    <AlarmContext.Provider
      value={{
        activeAlarm,
        stopAlarm,
        markAsTaken,
        snoozeAlarm,
        refreshMedicines: fetchMedicinesFromApi,
      }}
    >
      {children}
    </AlarmContext.Provider>
  );
};
