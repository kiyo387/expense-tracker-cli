import argparse
import datetime
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.json")


def load_expenses():
    """Return the list of expenses. Return [] if the file is missing or empty."""
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read expenses.json, starting with an empty list.", file=sys.stderr)
        return []
    if not isinstance(data, list):
        print("Warning: expenses.json has an unexpected format, starting empty.", file=sys.stderr)
        return []
    return data


def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=4)


def next_id(expenses):
    return max((e["id"] for e in expenses), default=0) + 1


def add_expense(amount, category, note, date):
    if not date:
        date = datetime.date.today().isoformat()

    expenses = load_expenses()
    expense_id = next_id(expenses)
    expense = {
        "id": expense_id,
        "amount": round(amount, 2),
        "category": category.lower().strip(),
        "note": note.strip(),
        "date": date,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added expense #{expense['id']}: {expense['amount']:.2f} in category '{expense['category']}' on {expense['date']}.")
    return 0


def list_expenses(category=None):
    expenses = load_expenses()
    if category:
        category = category.lower().strip()
        expenses = [e for e in expenses if e.get("category") == category]

    if not expenses:
        print("No expenses found.")
        return 0

    print(f"{'ID':<5} {'Amount':>10} {'Category':<15} {'Date':<12} Note")
    print("-" * 55)
    for e in sorted(expenses, key=lambda x: (x["date"], x["id"])):
        print(f"{e['id']:<5} {e['amount']:>10.2f} {e['category']:<15} {e['date']:<12} {e['note']}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("amount", type=float, help="Amount of the expense")
    add_parser.add_argument("category", type=str, help="Category of the expense")
    add_parser.add_argument("note", type=str, nargs="?", default="", help="Optional note for the expense")
    add_parser.add_argument("--date", type=str, help="Date of the expense in YYYY-MM-DD format (default: today)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all expenses")
    list_parser.add_argument("--category", type=str, help="Filter by category")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "add":
        return add_expense(args.amount, args.category, args.note, args.date)
    elif args.command == "list":
        return list_expenses(args.category)
    return 0


if __name__ == "__main__":
    sys.exit(main())
