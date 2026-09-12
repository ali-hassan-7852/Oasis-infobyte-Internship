"""
nlp_intent.py
Advanced-tier feature: parses user intent from free-form spoken sentences
instead of relying on rigid keyword matching.

Uses the Groq API (fast, free-tier LLM inference) to classify the user's
utterance into one of our supported intents and pull out any parameters
(e.g. a city name for weather, or a search topic).
"""

import os
import json
from groq import Groq

# Keep this list in sync with the handlers wired up in main.py
SUPPORTED_INTENTS = [
    "greeting",
    "get_time",
    "get_date",
    "web_search",
    "send_email",
    "set_reminder",
    "get_weather",
    "ask_question",
    "custom_command",
    "unknown",
]

SYSTEM_PROMPT = f"""You are an intent classifier for a voice assistant.
Given a user's spoken sentence, output ONLY a JSON object (no markdown, no
extra text) with this shape:

{{
  "intent": one of {SUPPORTED_INTENTS},
  "params": {{ ... any extracted parameters ... }}
}}

Guidelines for params:
- web_search -> {{"query": "<topic to search>"}}
- send_email -> {{"recipient": "<name or address if given>", "body_hint": "<what to say>"}}
- set_reminder -> {{"duration_seconds": <int>, "label": "<what the reminder is for>"}}
- get_weather -> {{"city": "<city name, or empty string if not given>"}}
- ask_question -> {{"question": "<the question, cleaned up>"}}
- custom_command -> {{"command_name": "<best guess at a matching custom command>"}}
- greeting, get_time, get_date, unknown -> params can be an empty object

Only output the JSON object, nothing else.
"""


class IntentParser:
    def __init__(self, api_key=None, model="llama-3.1-8b-instant"):
        api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not set. Export it as an environment variable "
                "or pass it directly to IntentParser()."
            )
        self.client = Groq(api_key=api_key)
        self.model = model

    def parse(self, utterance: str) -> dict:
        """
        Send the utterance to Groq and return a dict like:
        {"intent": "get_weather", "params": {"city": "Mumbai"}}

        Falls back to {"intent": "unknown", "params": {}} on any failure,
        so the rest of the assistant never crashes on a bad response.
        """
        if not utterance.strip():
            return {"intent": "unknown", "params": {}}

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": utterance},
                ],
                temperature=0,
                max_tokens=200,
            )
            raw = response.choices[0].message.content.strip()

            # Strip accidental markdown fences, just in case
            if raw.startswith("```"):
                raw = raw.strip("`")
                if raw.startswith("json"):
                    raw = raw[4:]

            parsed = json.loads(raw)

            if parsed.get("intent") not in SUPPORTED_INTENTS:
                parsed["intent"] = "unknown"
            parsed.setdefault("params", {})
            return parsed

        except Exception as e:
            print(f"[IntentParser error]: {e}")
            return {"intent": "unknown", "params": {}}
