"""
main.py
Tkinter GUI for the Random Password Generator (Advanced tier).

Run with: python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

from modules.generator import generate_password, PasswordGenerationError
from modules.strength import score_password

MAX_HISTORY = 5

STRENGTH_COLORS = {
    "Weak": "#d9534f",
    "Medium": "#f0ad4e",
    "Strong": "#5cb85c",
}


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Random Password Generator")
        self.geometry("440x520")
        self.resizable(False, False)

        # Session-only history - intentionally not written to disk so
        # generated passwords never persist between runs.
        self.history = []

        self._build_widgets()

    def _build_widgets(self):
        padding = {"padx": 12, "pady": 6}

        # --- Length control ---
        length_frame = ttk.LabelFrame(self, text="Password Length")
        length_frame.pack(fill="x", **padding)

        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(
            length_frame, from_=8, to=64, orient="horizontal",
            variable=self.length_var, command=self._on_length_scale_change
        )
        self.length_scale.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=8)

        self.length_spinbox = ttk.Spinbox(
            length_frame, from_=8, to=64, width=5, textvariable=self.length_var
        )
        self.length_spinbox.pack(side="left", padx=(0, 10))

        # --- Character type checkboxes ---
        types_frame = ttk.LabelFrame(self, text="Character Types")
        types_frame.pack(fill="x", **padding)

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        ttk.Checkbutton(types_frame, text="Uppercase (A-Z)", variable=self.use_upper).pack(anchor="w", padx=10)
        ttk.Checkbutton(types_frame, text="Lowercase (a-z)", variable=self.use_lower).pack(anchor="w", padx=10)
        ttk.Checkbutton(types_frame, text="Numbers (0-9)", variable=self.use_digits).pack(anchor="w", padx=10)
        ttk.Checkbutton(types_frame, text="Symbols (!@#$...)", variable=self.use_symbols).pack(anchor="w", padx=10)

        self.exclude_ambiguous = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            types_frame, text="Exclude ambiguous characters (0, O, 1, l, I)",
            variable=self.exclude_ambiguous
        ).pack(anchor="w", padx=10, pady=(4, 8))

        # --- Generate button ---
        ttk.Button(self, text="Generate Password", command=self._on_generate).pack(pady=10)

        # --- Result display ---
        result_frame = ttk.LabelFrame(self, text="Generated Password")
        result_frame.pack(fill="x", **padding)

        self.password_var = tk.StringVar(value="")
        self.password_entry = ttk.Entry(
            result_frame, textvariable=self.password_var,
            font=("Courier New", 13), justify="center", state="readonly"
        )
        self.password_entry.pack(fill="x", padx=10, pady=(10, 4))

        self.strength_label = ttk.Label(result_frame, text="", font=("Segoe UI", 10, "bold"))
        self.strength_label.pack(pady=(0, 8))

        self.copy_button = ttk.Button(
            result_frame, text="Copy to Clipboard", command=self._on_copy
        )
        self.copy_button.pack(pady=(0, 10))
        if not CLIPBOARD_AVAILABLE:
            self.copy_button.state(["disabled"])

        # --- History ---
        history_frame = ttk.LabelFrame(self, text="History (this session only, last 5)")
        history_frame.pack(fill="both", expand=True, **padding)

        self.history_listbox = tk.Listbox(history_frame, font=("Courier New", 10))
        self.history_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    # ---------- event handlers ----------

    def _on_length_scale_change(self, value):
        # ttk.Scale gives floats; keep the spinbox showing whole numbers.
        self.length_var.set(int(float(value)))

    def _on_generate(self):
        try:
            length = int(self.length_var.get())
        except (ValueError, tk.TclError):
            messagebox.showerror("Invalid length", "Please enter a valid number for length.")
            return

        try:
            password = generate_password(
                length=length,
                use_upper=self.use_upper.get(),
                use_lower=self.use_lower.get(),
                use_digits=self.use_digits.get(),
                use_symbols=self.use_symbols.get(),
                exclude_ambiguous=self.exclude_ambiguous.get(),
            )
        except PasswordGenerationError as e:
            messagebox.showerror("Can't generate password", str(e))
            return

        self.password_var.set(password)

        strength = score_password(password)
        self.strength_label.config(
            text=f"Strength: {strength}", foreground=STRENGTH_COLORS[strength]
        )

        # Per spec, the password copies to clipboard automatically as soon
        # as it's generated, not only when the Copy button is clicked.
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)

        self._add_to_history(password)

    def _on_copy(self):
        password = self.password_var.get()
        if not password:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(password)
        else:
            messagebox.showwarning(
                "Clipboard unavailable",
                "pyperclip isn't installed, so I can't copy automatically. "
                "Install it with: pip install pyperclip",
            )

    def _add_to_history(self, password: str):
        self.history.insert(0, password)
        self.history = self.history[:MAX_HISTORY]

        self.history_listbox.delete(0, tk.END)
        for i, pw in enumerate(self.history, start=1):
            self.history_listbox.insert(tk.END, f"{i}. {pw}")


if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
