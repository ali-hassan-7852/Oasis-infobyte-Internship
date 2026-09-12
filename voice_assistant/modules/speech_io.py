"""
speech_io.py
Handles all speech input (microphone -> text) and speech output (text -> voice).

Uses:
- speech_recognition: captures audio from the mic and sends it to Google's
  free web speech API for transcription (no key needed for basic use).
- pyttsx3: offline text-to-speech engine, works without internet.
"""

import speech_recognition as sr
import pyttsx3


class SpeechIO:
    def __init__(self, rate=175, volume=1.0, voice_index=None):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Set up the TTS engine once at startup - re-creating it every call
        # is slow and can cause audio glitches.
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

        if voice_index is not None:
            voices = self.engine.getProperty("voices")
            if 0 <= voice_index < len(voices):
                self.engine.setProperty("voice", voices[voice_index].id)

        # Calibrate for background noise once at startup.
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def speak(self, text: str):
        """Convert text to speech and play it out loud."""
        print(f"[Assistant]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, timeout=5, phrase_time_limit=8) -> str:
        """
        Listen on the microphone and return recognized text.
        Returns an empty string if nothing could be understood, so calling
        code can decide how to handle the "please repeat" flow.
        """
        with self.microphone as source:
            print("[Listening...]")
            try:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
            except sr.WaitTimeoutError:
                return ""

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"[You said]: {text}")
            return text
        except sr.UnknownValueError:
            # Speech was unintelligible
            return ""
        except sr.RequestError as e:
            print(f"[Speech recognition service error]: {e}")
            return ""
