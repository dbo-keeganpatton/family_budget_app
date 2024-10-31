import sqlite3 as sql

conn = sql.connect("database.db")
cur = conn.cursor()


dim_calendar_schema = """
CREATE TABLE dim_calendar (
    year_month_id INTEGER PRIMARY KEY,
    month_nbr INTEGER NOT NULL,
    month TEXT NOT NULL,
    year INTEGER NOT NULL
)
"""

dim_expense_schema = """
CREATE TABLE dim_expense (
    expense TEXT PRIMARY KEY,
    value INTEGER,
    priority BOOLEAN NOT NULL
)
"""

fact_payment_schema = """
CREATE TABLE fact_payment (
    date DATE NOT NULL,
    month TEXT NOT NULL,
    year_month_id INTEGER,
    expense TEXT,
    value INTEGER NOT NULL,
    paid BOOLEAN NOT NULL,
    FOREIGN KEY (year_month_id) REFERENCES dim_calendar (year_month_id),
    FOREIGN KEY (expense) REFERENCES dim_expense (expense)
)
"""

add_column = """
ALTER TABLE dim_expense
ADD COLUMN current_ind BOOLEAN
"""


