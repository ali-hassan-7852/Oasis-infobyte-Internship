"""
reminders.py
Sets a timed reminder that triggers an audible alert (spoken out loud)
after a specified duration, without blocking the rest of the assistant.
"""

import threading


class ReminderManager:
    def __init__(self, speak_callback):
        """
        speak_callback: a function like SpeechIO.speak(text) used to
        announce the reminder when it fires.
        """
        self._speak = speak_callback
        self._active_timers = []

    def set_reminder(self, duration_seconds: int, label: str = "your reminder") -> str:
        if duration_seconds <= 0:
            return "I need a positive duration to set a reminder."

        def fire():
            self._speak(f"Reminder: {label}")

        timer = threading.Timer(duration_seconds, fire)
        timer.daemon = True  # don't block program exit
        timer.start()
        self._active_timers.append(timer)

        minutes = duration_seconds / 60
        return f"Okay, I'll remind you about {label} in {minutes:.1f} minutes."

    def cancel_all(self):
        for t in self._active_timers:
            t.cancel()
        self._active_timers.clear()
