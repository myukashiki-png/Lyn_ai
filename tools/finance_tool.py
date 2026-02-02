import csv
from datetime import datetime

FILE = "memory/finance.csv"

def add_expense(amount, category):
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), amount, category])
    return f"Pengeluaran {amount} dicatat untuk {category}."

