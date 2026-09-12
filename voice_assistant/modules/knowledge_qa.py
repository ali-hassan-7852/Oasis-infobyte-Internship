"""
knowledge_qa.py
Answers general knowledge questions using the Groq API as the QA backend.

We chose an LLM-backed QA API over a small local JSON knowledge base
because it handles open-ended, free-form questions instead of only exact
matches from a fixed list of Q&A pairs.
"""

import os
from groq import Groq


class KnowledgeQA:
    def __init__(self, api_key=None, model="llama-3.1-8b-instant"):
        api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set.")
        self.client = Groq(api_key=api_key)
        self.model = model

    def answer(self, question: str) -> str:
        if not question.strip():
            return "I didn't catch a question to answer."

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a voice assistant. Answer the user's "
                            "question in 1-3 short spoken sentences. No "
                            "markdown, no bullet points, since this will "
                            "be read aloud."
                        ),
                    },
                    {"role": "user", "content": question},
                ],
                temperature=0.3,
                max_tokens=150,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"I couldn't look that up right now: {e}"
