"""
main.py
Tkinter GUI for the BMI Calculator (Advanced tier).

Run with: python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.bmi_logic import (
    parse_and_validate,
    calculate_bmi,
    classify_bmi,
    InputValidationError,
    CATEGORY_COLORS,
)
from modules.database import BMIDatabase, DatabaseError


class BMICalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator")
        self.geometry("420x460")
        self.resizable(False, False)

        try:
            self.db = BMIDatabase()
        except DatabaseError as e:
            messagebox.showerror("Database error", str(e))
            self.db = None

        self._build_widgets()
        self._refresh_user_dropdown()

    # ---------- UI construction ----------

    def _build_widgets(self):
        padding = {"padx": 14, "pady": 6}

        # --- User selection (multi-user support) ---
        user_frame = ttk.LabelFrame(self, text="User")
        user_frame.pack(fill="x", **padding)

        self.username_var = tk.StringVar()
        self.user_combo = ttk.Combobox(user_frame, textvariable=self.username_var)
        self.user_combo.pack(fill="x", padx=10, pady=10)
        self.user_combo.set("Type a name (new or existing)")
        self.user_combo.bind("<FocusIn>", self._clear_placeholder)

        # --- Inputs ---
        input_frame = ttk.LabelFrame(self, text="Measurements")
        input_frame.pack(fill="x", **padding)

        ttk.Label(input_frame, text="Weight (kg):").grid(row=0, column=0, sticky="w", padx=10, pady=6)
        self.weight_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.weight_var).grid(row=0, column=1, padx=10, pady=6, sticky="ew")

        ttk.Label(input_frame, text="Height (m):").grid(row=1, column=0, sticky="w", padx=10, pady=6)
        self.height_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.height_var).grid(row=1, column=1, padx=10, pady=6, sticky="ew")

        input_frame.columnconfigure(1, weight=1)

        # --- Calculate button ---
        ttk.Button(self, text="Calculate", command=self._on_calculate).pack(pady=10)

        # --- Result display, color-coded ---
        result_frame = ttk.LabelFrame(self, text="Result")
        result_frame.pack(fill="x", **padding)

        self.result_label = tk.Label(
            result_frame, text="Enter your details and click Calculate",
            font=("Segoe UI", 12, "bold"), wraplength=350, justify="center"
        )
        self.result_label.pack(padx=10, pady=14)

        # --- History / graph ---
        ttk.Button(self, text="View BMI Trend", command=self._on_view_trend).pack(pady=6)

    def _clear_placeholder(self, event):
        if self.username_var.get() == "Type a name (new or existing)":
            self.username_var.set("")

    def _refresh_user_dropdown(self):
        if not self.db:
            return
        try:
            users = self.db.get_all_usernames()
            self.user_combo["values"] = users
        except DatabaseError as e:
            messagebox.showerror("Database error", str(e))

    # ---------- event handlers ----------

    def _on_calculate(self):
        username = self.username_var.get().strip()
        if not username or username == "Type a name (new or existing)":
            messagebox.showerror("Missing name", "Please enter a name to track this record under.")
            return

        try:
            weight, height = parse_and_validate(self.weight_var.get(), self.height_var.get())
        except InputValidationError as e:
            messagebox.showerror("Invalid input", str(e))
            return

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)
        color = CATEGORY_COLORS[category]

        self.result_label.config(
            text=f"BMI: {bmi:.2f}  —  {category}", foreground=color
        )

        if self.db:
            try:
                self.db.add_record(username, weight, height, bmi, category)
                self._refresh_user_dropdown()
            except DatabaseError as e:
                messagebox.showerror(
                    "Couldn't save record",
                    f"Your BMI was calculated, but saving to the database failed:\n{e}"
                )

    def _on_view_trend(self):
        username = self.username_var.get().strip()
        if not username or username == "Type a name (new or existing)":
            messagebox.showerror("Missing name", "Enter or select a user first.")
            return

        if not self.db:
            messagebox.showerror("Database unavailable", "No database connection is available.")
            return

        try:
            records = self.db.get_records_for_user(username)
        except DatabaseError as e:
            messagebox.showerror("Couldn't load history", str(e))
            return

        if not records:
            messagebox.showinfo("No history", f"No saved BMI records found for '{username}' yet.")
            return

        TrendWindow(self, username, records)


class TrendWindow(tk.Toplevel):
    """A separate window showing a matplotlib line chart of a user's
    BMI trend over time."""

    def __init__(self, parent, username, records):
        super().__init__(parent)
        self.title(f"BMI Trend — {username}")
        self.geometry("600x450")

        dates = [r["recorded_at"][:10] for r in records]  # just the date part
        bmis = [r["bmi"] for r in records]

        fig = Figure(figsize=(5.5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, bmis, marker="o", linestyle="-", color="#2f7dd1")
        ax.set_title(f"BMI Trend for {username}")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        ax.axhspan(18.5, 25, color="#2fa84f", alpha=0.08)  # normal range shading
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    app = BMICalculatorApp()
    app.mainloop()
