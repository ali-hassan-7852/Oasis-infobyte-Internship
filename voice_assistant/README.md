# Python Voice Assistant (Advanced Tier)

A voice-controlled assistant built for the Python Programming internship
track. It listens for spoken commands, understands intent using an LLM
(Groq) rather than plain keyword matching, and can tell the time/date,
search the web, check the weather, send email, set reminders, answer
general knowledge questions, and run custom voice commands.

## Features

**Beginner tier (all included):**
- Capture voice input via microphone (`speech_recognition`)
- Respond to greetings
- Tell current time and date
- Web search on a spoken topic
- Graceful error handling ("please repeat")
- Text-to-speech for every response (`pyttsx3`)

**Advanced tier:**
- Natural language intent parsing from free-form sentences (Groq LLM),
  not just keyword matching
- Send email via voice command (`smtplib`)
- Set a timed reminder with an audible alert
- Live weather via the OpenWeatherMap free API
- General knowledge Q&A via Groq
- Custom commands, addable via config file or voice
- Documented privacy/data handling (below)

## Project Structure

```
voice_assistant/
├── main.py                  # entry point, wires everything together
├── modules/
│   ├── speech_io.py          # mic capture + text-to-speech
│   ├── nlp_intent.py         # Groq-based intent parser
│   ├── weather.py             # OpenWeatherMap client
│   ├── email_sender.py        # smtplib wrapper
│   ├── reminders.py           # threaded timed reminders
│   ├── knowledge_qa.py        # Groq-based general knowledge QA
│   └── custom_commands.py     # user-defined commands
├── config/
│   └── commands.json          # custom command definitions
├── requirements.txt
└── README.md
```

## Setup

1. **Install system dependencies for PyAudio** (needed by speech_recognition
   for microphone access):
   - Ubuntu/Debian: `sudo apt-get install portaudio19-dev python3-pyaudio`
   - macOS: `brew install portaudio`
   - Windows: usually works with just `pip install pyaudio`; if it fails,
     install the prebuilt wheel from pipwin (`pip install pipwin && pipwin install pyaudio`)

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   export GROQ_API_KEY="your_groq_api_key"
   export OPENWEATHER_API_KEY="your_openweathermap_key"     # optional, for weather
   export ASSISTANT_EMAIL_ADDRESS="your_test_account@gmail.com"   # optional, for email
   export ASSISTANT_EMAIL_APP_PASSWORD="your_app_password"        # optional, for email
   ```
   On Windows (PowerShell): use `$env:GROQ_API_KEY="..."` instead.

   - Groq key: sign up free at https://console.groq.com
   - OpenWeatherMap key: sign up free at https://openweathermap.org/api
     (Current Weather Data, free plan — no credit card needed)
   - Email: **use a dummy/test account**, never a personal one. For Gmail,
     turn on 2FA and generate an "App Password" instead of using the real
     account password.

4. **Run it:**
   ```bash
   python main.py
   ```
   Say "exit", "quit", or "goodbye" to stop.

## Privacy Consideration

This assistant processes the following data, and where it goes:

- **Voice audio**: captured locally by the microphone, then sent to
  Google's speech recognition web service (via the `speech_recognition`
  library's default recognizer) to be transcribed to text. Audio is not
  stored on disk by this project.
- **Transcribed text (your spoken commands)**: sent to the Groq API for
  intent classification and, for general knowledge questions, sent again
  to Groq to generate an answer. Groq processes this per their API terms;
  no conversation history is persisted by this project between runs.
- **Weather queries**: only the city name is sent to OpenWeatherMap; no
  personal data is included.
- **Email feature**: recipient address and message body are sent via
  SMTP to your configured mail provider (e.g. Gmail) using the
  credentials you provide. Credentials are read from environment
  variables, never hard-coded or logged.
- **Custom commands**: stored locally in `config/commands.json` in plain
  text. Don't put sensitive information in a custom command's response.
- **No data is sent anywhere else.** No analytics, no third-party
  tracking. All API keys/credentials are supplied by the user via
  environment variables and are not committed to source control (see
  `.gitignore` recommendation below).

**Recommendation:** add a `.gitignore` entry for any `.env` file you use
to store these keys locally, so you never accidentally commit credentials.

## Notes on Design Decisions

- Chose **Groq** for both intent parsing and the QA feature (instead of a
  static local knowledge base) since it handles open-ended, free-form
  input rather than requiring exact keyword matches — this is what makes
  the "advanced" NLU checklist item work.
- Reminders use `threading.Timer` so the assistant isn't blocked while
  waiting for the reminder to fire.
- Custom commands are canned text responses rather than arbitrary code
  execution from voice input, to avoid accidentally creating a way to
  run arbitrary commands just by talking to the mic.

## Known Limitations

- Requires an internet connection (speech recognition, Groq, weather,
  and email all call external services).
- `pyttsx3` voice quality/available voices depend on the OS's installed
  TTS engines (SAPI5 on Windows, NSSpeechSynthesizer on macOS, espeak on
  Linux).
- Email sending is tested against Gmail's SMTP; other providers may need
  a different `smtp_server`/`smtp_port` in `email_sender.py`.

## Sources / References

- `speech_recognition` docs: https://pypi.org/project/SpeechRecognition/
- OpenWeatherMap API docs: https://openweathermap.org/current
- Groq API docs: https://console.groq.com/docs
