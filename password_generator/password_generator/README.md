# Random Password Generator (Advanced Tier)

A tkinter GUI tool that generates cryptographically secure, random
passwords based on user-defined criteria, for the Python Programming
internship track.

## Features

**Beginner tier (all included):**
- Prompt for desired password length (minimum 8 enforced)
- Choose which character types to include (uppercase, lowercase,
  numbers, symbols) — at least 2 required
- Generate and display a password matching the criteria
- Input validation with clear error messages
- Generate another password without restarting

**Advanced tier:**
- GUI window (tkinter) with a slider + spinbox for length, and
  checkboxes for character type selection
- Uses the `secrets` module (not `random`) for cryptographically secure
  generation
- Password strength indicator (Weak / Medium / Strong), color-coded
- Guarantees at least one character from each selected type
- "Copy to Clipboard" button (`pyperclip`) — password also copies
  automatically the moment it's generated
- Option to exclude ambiguous characters (0, O, 1, l, I)
- Session history showing the last 5 generated passwords (in-memory
  only — never written to disk, for security)

## Project Structure

```
password_generator/
├── main.py                # tkinter GUI, entry point
├── modules/
│   ├── generator.py        # core password generation (secrets-based)
│   └── strength.py         # password strength scoring
├── requirements.txt
└── README.md
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Note: `tkinter` ships with most standard Python installs. On Linux, if
   it's missing: `sudo apt-get install python3-tk`.

2. **Run it:**
   ```bash
   python main.py
   ```

## Design Decisions

- **`secrets` instead of `random`**: `random` uses a Mersenne Twister PRNG
  that is predictable if enough outputs are observed — fine for
  simulations, not safe for anything security-related. `secrets` is
  built on the OS's cryptographically secure random source
  (`os.urandom`), which is the correct tool for generating passwords,
  tokens, or keys. See: https://docs.python.org/3/library/secrets.html
- **Guaranteed character coverage**: rather than generating purely
  randomly and hoping every selected type shows up, the generator
  explicitly picks one character from each selected type first, then
  fills the rest of the length from the combined pool, then shuffles
  with `secrets.SystemRandom().shuffle()` so the guaranteed characters
  aren't predictably placed at the start.
- **History kept in memory only**: writing generated passwords to disk,
  even temporarily, creates a place they could leak from. Keeping the
  list in a Python variable means it disappears the moment the app
  closes.
- **Ambiguous-character filtering falls back safely**: if excluding
  ambiguous characters would wipe out an entire selected character
  type (e.g., a symbol set with no ambiguous characters to begin with),
  the filter is skipped for that type instead of silently producing a
  shorter-than-requested pool.

## Known Limitations

- No password persistence by design (history resets on restart) — this
  is intentional, not a bug.
- Strength scoring is a simple length + diversity heuristic for display
  purposes, not a formal entropy/zxcvbn-style calculation.
- If `pyperclip` isn't installed or clipboard access isn't available on
  the OS, the Copy button is disabled but password generation still
  works fully.

## Sources / References

- Python `secrets` module docs: https://docs.python.org/3/library/secrets.html
- Python `tkinter` docs: https://docs.python.org/3/library/tkinter.html
- `pyperclip` on PyPI: https://pypi.org/project/pyperclip/
