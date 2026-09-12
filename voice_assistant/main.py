"""
main.py
Entry point for the voice assistant (Advanced tier).

Beginner-tier features (all included):
- Capture voice input via microphone
- Respond to "Hello" with a greeting
- Tell current time/date
- Web search on a spoken topic
- Graceful error handling / "please repeat"
- Text-to-speech for every response

Advanced-tier features (this file):
- NLU intent parsing (modules/nlp_intent.py) instead of keyword matching
- Email via voice command
- Timed reminders with audible alert
- Live weather via OpenWeatherMap
- General knowledge QA
- Custom commands via config file / voice
- Privacy handling documented in README.md
"""

import datetime
import webbrowser
import urllib.parse

from modules.speech_io import SpeechIO
from modules.nlp_intent import IntentParser
from modules.weather import WeatherService
from modules.email_sender import EmailSender
from modules.reminders import ReminderManager
from modules.knowledge_qa import KnowledgeQA
from modules.custom_commands import CustomCommands

EXIT_WORDS = {"exit", "quit", "stop", "goodbye", "bye"}


class VoiceAssistant:
    def __init__(self):
        self.speech = SpeechIO()
        self.intent_parser = IntentParser()
        self.weather = WeatherService()
        self.email = EmailSender()
        self.reminders = ReminderManager(speak_callback=self.speech.speak)
        self.qa = KnowledgeQA()
        self.custom_commands = CustomCommands()

    # ---------- individual feature handlers ----------

    def handle_greeting(self):
        self.speech.speak("Hello! How can I help you today?")

    def handle_get_time(self):
        now = datetime.datetime.now().strftime("%I:%M %p")
        self.speech.speak(f"The current time is {now}.")

    def handle_get_date(self):
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.speech.speak(f"Today's date is {today}.")

    def handle_web_search(self, query: str):
        if not query:
            self.speech.speak("What would you like me to search for?")
            return
        url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
        webbrowser.open(url)
        self.speech.speak(f"Here's what I found for {query}.")

    def handle_send_email(self, recipient: str, body_hint: str):
        if not recipient:
            self.speech.speak("Who should I send the email to?")
            return
        subject = "Message from your voice assistant"
        body = body_hint or "This is a test message sent by voice command."
        result = self.email.send_email(recipient, subject, body)
        self.speech.speak(result)

    def handle_set_reminder(self, duration_seconds: int, label: str):
        result = self.reminders.set_reminder(duration_seconds, label or "your reminder")
        self.speech.speak(result)

    def handle_get_weather(self, city: str):
        result = self.weather.get_weather(city)
        self.speech.speak(result)

    def handle_ask_question(self, question: str):
        result = self.qa.answer(question)
        self.speech.speak(result)

    def handle_custom_command(self, command_name: str):
        result = self.custom_commands.run(command_name)
        self.speech.speak(result)

    def handle_unknown(self):
        self.speech.speak("Sorry, I didn't quite catch that. Could you repeat it?")

    # ---------- dispatch ----------

    def dispatch(self, intent: str, params: dict):
        if intent == "greeting":
            self.handle_greeting()
        elif intent == "get_time":
            self.handle_get_time()
        elif intent == "get_date":
            self.handle_get_date()
        elif intent == "web_search":
            self.handle_web_search(params.get("query", ""))
        elif intent == "send_email":
            self.handle_send_email(
                params.get("recipient", ""), params.get("body_hint", "")
            )
        elif intent == "set_reminder":
            self.handle_set_reminder(
                int(params.get("duration_seconds", 0)), params.get("label", "")
            )
        elif intent == "get_weather":
            self.handle_get_weather(params.get("city", ""))
        elif intent == "ask_question":
            self.handle_ask_question(params.get("question", ""))
        elif intent == "custom_command":
            self.handle_custom_command(params.get("command_name", ""))
        else:
            self.handle_unknown()

    # ---------- main loop ----------

    def run(self):
        self.speech.speak("Voice assistant ready. Say something!")
        while True:
            utterance = self.speech.listen()

            if not utterance:
                self.speech.speak("Sorry, I didn't hear that clearly. Please repeat.")
                continue

            if utterance.strip().lower() in EXIT_WORDS:
                self.speech.speak("Goodbye!")
                break

            parsed = self.intent_parser.parse(utterance)
            self.dispatch(parsed["intent"], parsed["params"])


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
