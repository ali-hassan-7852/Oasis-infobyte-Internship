"""
database.py
SQLite storage layer for BMI records, supporting multiple named users
and historical trend data. All database errors are caught here and
surfaced as DatabaseError with a friendly message, so the GUI layer
never has to deal with raw sqlite3 exceptions.
"""

import sqlite3
import os
from datetime import datetime

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "bmi_records.db")


class DatabaseError(Exception):
    """Raised on any read/write failure against the BMI records database."""


class BMIDatabase:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._init_schema()

    def _connect(self):
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            raise DatabaseError(f"Couldn't connect to the database: {e}")

    def _init_schema(self):
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS bmi_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        weight_kg REAL NOT NULL,
                        height_m REAL NOT NULL,
                        bmi REAL NOT NULL,
                        category TEXT NOT NULL,
                        recorded_at TEXT NOT NULL
                    )
                    """
                )
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Couldn't set up the database: {e}")

    def add_record(self, username: str, weight_kg: float, height_m: float,
                    bmi: float, category: str) -> None:
        username = username.strip()
        if not username:
            raise DatabaseError("A username is required to save a record.")

        timestamp = datetime.now().isoformat(timespec="seconds")
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO bmi_records
                        (username, weight_kg, height_m, bmi, category, recorded_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (username, weight_kg, height_m, bmi, category, timestamp),
                )
                conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Couldn't save the record: {e}")

    def get_records_for_user(self, username: str) -> list[dict]:
        try:
            with self._connect() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    """
                    SELECT weight_kg, height_m, bmi, category, recorded_at
                    FROM bmi_records
                    WHERE username = ?
                    ORDER BY recorded_at ASC
                    """,
                    (username.strip(),),
                )
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            raise DatabaseError(f"Couldn't load history: {e}")

    def get_all_usernames(self) -> list[str]:
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT DISTINCT username FROM bmi_records ORDER BY username ASC"
                )
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            raise DatabaseError(f"Couldn't load user list: {e}")
