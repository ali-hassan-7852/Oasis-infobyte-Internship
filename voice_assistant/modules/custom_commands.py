"""
custom_commands.py
Lets users define their own simple voice commands in a config file
(config/commands.json), and add new ones on the fly by voice.

Each custom command maps a trigger name to a canned spoken response.
This is intentionally simple (no arbitrary code execution from voice
input, for safety) - it's meant for things like:
  "turn on my desk light routine" -> "Sure, running your desk light routine."
"""

import json
import os

DEFAULT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "config", "commands.json"
)


class CustomCommands:
    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.commands = self._load()

    def _load(self) -> dict:
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.commands, f, indent=2)

    def run(self, command_name: str) -> str:
        command_name = command_name.strip().lower()
        if command_name in self.commands:
            return self.commands[command_name]
        return (
            f"I don't have a custom command called '{command_name}' yet. "
            f"You can add one by saying: add command."
        )

    def add_command(self, name: str, response: str) -> str:
        name = name.strip().lower()
        self.commands[name] = response
        self._save()
        return f"Got it, I've saved the command '{name}'."
