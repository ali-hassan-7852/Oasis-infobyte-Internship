# Oasis InfoBytes Internship — Python Programming Track

**Intern:** Ali Hassan ([@ali-hassan-7852](https://github.com/ali-hassan-7852))
**Organization:** Oasis InfoBytes
**Track:** Python Programming
**Submission Date:** September 12, 2026

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-2fa84f)
![Tier](https://img.shields.io/badge/Tier-Advanced-e0972c)

---

## About This Repository

This repository contains my submissions for the Oasis InfoBytes Python
Programming internship track. The track's completion rule required at
least 3 of 5 available tasks, each buildable at a Beginner or Advanced
level. I chose to complete **3 tasks at the Advanced tier**, since I
wanted the extra practice with GUI development, external APIs, and data
persistence rather than sticking to command-line scripts.

Each project lives in its own folder with its own `README.md` covering
setup, features, and the reasoning behind key design decisions.

## Table of Contents

- [Projects](#projects)
  - [1. Voice Assistant](#1-voice-assistant)
  - [2. BMI Calculator](#2-bmi-calculator)
  - [3. Random Password Generator](#3-random-password-generator)
- [Tech Stack Summary](#tech-stack-summary)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)

---

## Projects

### 1. Voice Assistant

A Python voice assistant that listens for spoken commands and responds
with useful actions — greetings, time/date, web search, live weather,
email, timed reminders, and general knowledge Q&A — using natural
language intent parsing instead of rigid keyword matching.

| | |
|---|---|
| **Tier** | Advanced |
| **Core Libraries** | `speech_recognition`, `pyttsx3`, `groq`, `requests`, `smtplib` |
| **Highlights** | LLM-based intent parsing (Groq), live weather (OpenWeatherMap), voice-triggered email, timed reminders, general knowledge QA, custom voice commands, documented data-privacy handling |

📂 [`/voice_assistant`](./voice_assistant) · [Project README](./voice_assistant/README.md)

### 2. BMI Calculator

A tkinter GUI application that calculates BMI, classifies it into
health categories with color-coded feedback, supports multiple named
users, and stores historical records in SQLite with a matplotlib trend
graph.

| | |
|---|---|
| **Tier** | Advanced |
| **Core Libraries** | `tkinter`, `sqlite3`, `matplotlib` |
| **Highlights** | Full GUI (no CLI), color-coded results by category, multi-user record tracking, SQLite persistence, embedded BMI trend line chart, error handling for DB read/write failures |

📂 [`/bmi_calculator`](./bmi_calculator) · [Project README](./bmi_calculator/README.md)

### 3. Random Password Generator

A tkinter GUI tool that generates cryptographically secure passwords
based on user-defined length and character-type criteria, with a
strength indicator and clipboard integration.

| | |
|---|---|
| **Tier** | Advanced |
| **Core Libraries** | `tkinter`, `secrets`, `pyperclip` |
| **Highlights** | Slider + spinbox length control, guaranteed character-type coverage, Weak/Medium/Strong strength indicator, auto-copy to clipboard, ambiguous-character exclusion, in-memory session history (not persisted, by design) |

📂 [`/password_generator`](./password_generator) · [Project README](./password_generator/README.md)

---

## Tech Stack Summary

| Category | Tools Used |
|---|---|
| GUI | `tkinter` |
| Data & Storage | `sqlite3` |
| Visualization | `matplotlib` |
| APIs & AI | `groq` (LLM), OpenWeatherMap API |
| Speech | `speech_recognition`, `pyttsx3` |
| Security | `secrets`, `smtplib`, `pyperclip` |

## Repository Structure

```
oasis-infobytes-python-internship/
├── voice_assistant/
│   ├── main.py
│   ├── modules/
│   ├── config/
│   ├── requirements.txt
│   └── README.md
├── bmi_calculator/
│   ├── main.py
│   ├── modules/
│   ├── requirements.txt
│   └── README.md
├── password_generator/
│   ├── main.py
│   ├── modules/
│   ├── requirements.txt
│   └── README.md
└── README.md   (this file)
```

## Getting Started

Each project is independent and has its own dependencies. To run any of
them:

```bash
cd <project_folder>
pip install -r requirements.txt
python main.py
```

See each project's own README for API keys needed, environment
variables, and platform-specific setup notes (e.g. `tkinter` or
`PyAudio` system dependencies).

---

*Submitted as part of the Oasis InfoBytes Python Programming internship
track completion requirements.*
