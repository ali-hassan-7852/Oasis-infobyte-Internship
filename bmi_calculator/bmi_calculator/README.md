# BMI Calculator (Advanced Tier)

A tkinter GUI application that calculates Body Mass Index (BMI),
classifies it into health categories, tracks records per named user in
a SQLite database, and graphs BMI trends over time with matplotlib.

## Features

**Beginner tier (all included):**
- Prompt for weight (kg) and height (m)
- Calculate BMI using `weight / height²`
- Classify into Underweight (<18.5), Normal (18.5–24.9), Overweight
  (25–29.9), Obese (≥30)
- Display BMI rounded to 2 decimal places, with category
- Input validation: rejects non-numeric and negative input with a clear
  error message

**Advanced tier:**
- Full GUI built with tkinter — no command line
- Labeled input fields and a Calculate button
- Color-coded result (green = normal, red = obese, orange = overweight,
  blue = underweight)
- Multi-user support: save BMI records under different named users
- Historical records stored in an SQLite database (`bmi_records.db`,
  created automatically on first run)
- Graph view: line chart of a user's BMI trend over time via matplotlib,
  embedded directly in a tkinter window
- Error handling for database read/write failures — the GUI stays usable
  and shows a clear message instead of crashing

## Project Structure

```
bmi_calculator/
├── main.py                # tkinter GUI, entry point
├── modules/
│   ├── bmi_logic.py         # BMI calculation, classification, validation
│   └── database.py          # SQLite storage layer
├── requirements.txt
└── README.md
```

(`bmi_records.db` is created next to this folder the first time you run
the app — it's not included in the project since it's user data, not
source code.)

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   `tkinter` and `sqlite3` ship with standard Python. On Linux, if
   tkinter is missing: `sudo apt-get install python3-tk`.

2. **Run it:**
   ```bash
   python main.py
   ```

3. Type a name in the "User" field, enter weight/height, and click
   **Calculate**. Each calculation is saved under that name automatically.
   Click **View BMI Trend** to see a line chart of that user's BMI history.

## Design Decisions

- **Logic, storage, and UI are separated** into `bmi_logic.py`,
  `database.py`, and `main.py`. This means the BMI math and validation
  can be unit-tested without opening a GUI window, and the storage layer
  could be swapped (e.g. for CSV) without touching the calculation logic.
- **SQLite over CSV**: chosen because it makes per-user filtering and
  chronological ordering (`ORDER BY recorded_at`) trivial with SQL,
  and avoids hand-parsing a CSV file for the trend graph.
- **All database calls are wrapped and re-raised as `DatabaseError`**
  in `database.py`, so `main.py` never has to catch raw `sqlite3.Error`
  — it just shows whatever message it's given in a message box. This
  satisfies the "error handling for read/write failures" requirement
  without scattering try/except blocks across the GUI code.
- **Height sanity check**: if someone enters height in centimeters by
  mistake (e.g. `175`), the result would be a wildly wrong BMI with no
  visible error. A bounds check (`height > 3`) catches this common
  mistake with a specific, actionable message instead of a silently
  wrong answer.
- **Normal-range shading on the trend graph** (`ax.axhspan(18.5, 25, ...)`)
  gives a quick visual reference for whether the user's BMI history sits
  inside the healthy range, without needing extra text labels.

## Known Limitations

- The database file (`bmi_records.db`) is a single shared SQLite file —
  fine for one local user with several tracked names, not designed for
  concurrent multi-machine access.
- No authentication: any "user" is just a name typed into the field,
  not a secured account.
- The height sanity bound (3 meters) and weight bound (500 kg) are
  simple guardrails against obvious typos, not medical limits.

## Sources / References

- Python `sqlite3` docs: https://docs.python.org/3/library/sqlite3.html
- Python `tkinter` docs: https://docs.python.org/3/library/tkinter.html
- Matplotlib `FigureCanvasTkAgg` docs: https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
- BMI category thresholds: WHO / CDC standard adult BMI classification
