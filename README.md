# Expense Tracker CLI

A lightweight, zero-dependency command-line expense tracker written in Python. It stores your expenses locally in JSON format and provides fast, convenient commands to record, categorize, inspect, and export your spending.

---

## Features

- **Add Expenses**: Track amount, category, optional note, and custom or default date (today).
- **Collision-free IDs**: Auto-increments IDs based on the highest existing ID (`max(ids) + 1`), avoiding ID collisions after deletions.
- **Filtering**: Filter expenses by category (case-insensitive) or by month (`YYYY-MM`).
- **Totals & Summary**: View spending totals by category or inspect an overall category-wise breakdown.
- **CSV Export**: Export all recorded expenses to a `.csv` file for external spreadsheet analysis.
- **Zero External Dependencies**: Implemented entirely with Python's standard library (`argparse`, `json`, `datetime`, `csv`, `os`, `sys`).

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kiyo387/expense-tracker-cli.git
   cd expense-tracker-cli
   ```

2. **Requirements:**
   - Python 3.8 or higher.
   - No external libraries or `pip install` required.

---

## Usage Examples

Run `python expense.py` with no arguments to see the available commands and help menu:

```bash
python expense.py
```

### 1. Add an Expense
```bash
# Basic usage: amount, category, and optional note
python expense.py add 25.50 food "Lunch with friends"

# With an optional specific date (YYYY-MM-DD)
python expense.py add 45.00 transport "Train pass" --date 2026-11-01

# Note is optional
python expense.py add 12.00 coffee
```

### 2. List Expenses
```bash
# List all expenses
python expense.py list

# Filter by category
python expense.py list --category food

# Filter by month (YYYY-MM)
python expense.py list --month 2026-11

# Combine filters
python expense.py list --category food --month 2026-11
```

*Output sample:*
```
ID    Amount     Category        Date         Note
-------------------------------------------------------
1          25.50 food            2026-11-01   Train pass
2          12.00 coffee          2026-11-07   
```

### 3. Total Spending
```bash
# Total for all expenses
python expense.py total

# Total for a specific category
python expense.py total --category food

# Total for a specific month
python expense.py total --month 2026-11
```

### 4. Summary Breakdown
Generates a sorted summary table of all expenses grouped by category:
```bash
python expense.py summary
```

*Output sample:*
```
Category             Total
--------------------------
food                 65.50
transport            45.00
coffee               12.00
--------------------------
All                 122.50
```

### 5. Export to CSV
Export your expenses into a CSV file for spreadsheets like Excel or Google Sheets:
```bash
# Export to default expenses.csv
python expense.py export

# Specify custom file destination
python expense.py export --output november_expenses.csv
```

### 6. Delete an Expense
Delete an expense by its unique ID:
```bash
python expense.py delete 1
```

---

## Storage Format

Expenses are stored locally in an `expenses.json` file created in the project directory. The file contains an array of JSON objects with the following schema:

```json
[
    {
        "id": 1,
        "amount": 25.50,
        "category": "food",
        "note": "Lunch with friends",
        "date": "2026-11-07"
    },
    {
        "id": 2,
        "amount": 45.00,
        "category": "transport",
        "note": "Train pass",
        "date": "2026-11-01"
    }
]
```

`expenses.json` and any exported `.csv` files are ignored by git via `.gitignore` so your personal financial data stays private.
