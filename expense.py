import argparse
import csv
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


def filter_expenses(expenses, category=None, month=None):
    if category:
        category = category.lower().strip()
        expenses = [e for e in expenses if e.get("category") == category]
    if month:
        month = month.strip()
        expenses = [e for e in expenses if e.get("date", "").startswith(month)]
    return expenses


def add_expense(amount, category, note, date):
    if amount <= 0:
        print("Error: Amount must be a positive number.", file=sys.stderr)
        return 1

    category = category.lower().strip()
    if not category:
        print("Error: Category cannot be empty.", file=sys.stderr)
        return 1

    if not date:
        date = datetime.date.today().isoformat()
    else:
        try:
            date = datetime.date.fromisoformat(date).isoformat()
        except ValueError:
            print("Error: Date must be in YYYY-MM-DD format.", file=sys.stderr)
            return 1

    expenses = load_expenses()
    expense_id = next_id(expenses)
    expense = {
        "id": expense_id,
        "amount": round(amount, 2),
        "category": category,
        "note": (note or "").strip(),
        "date": date,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added expense #{expense['id']}: {expense['amount']:.2f} in category '{expense['category']}' on {expense['date']}.")
    return 0


def list_expenses(category=None, month=None):
    expenses = filter_expenses(load_expenses(), category, month)
    if not expenses:
        print("No expenses found.")
        return 0

    print(f"{'ID':<5} {'Amount':>10} {'Category':<15} {'Date':<12} Note")
    print("-" * 55)
    for e in sorted(expenses, key=lambda x: (x["date"], x["id"])):
        print(f"{e['id']:<5} {e['amount']:>10.2f} {e['category']:<15} {e['date']:<12} {e['note']}")
    return 0


def total_expenses(category=None, month=None):
    expenses = filter_expenses(load_expenses(), category, month)
    total = sum(e["amount"] for e in expenses)
    details = []
    if category:
        details.append(f"category '{category}'")
    if month:
        details.append(f"month '{month}'")

    label = f" in {', '.join(details)}" if details else ""
    print(f"Total expenses{label}: {total:.2f}")
    return 0


def delete_expense(expense_id):
    expenses = load_expenses()
    remaining = [e for e in expenses if e.get("id") != expense_id]
    if len(remaining) == len(expenses):
        print(f"Error: Expense with ID {expense_id} not found.", file=sys.stderr)
        return 1
    save_expenses(remaining)
    print(f"Deleted expense #{expense_id}.")
    return 0


def summary():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return 0
    totals = {}
    for e in expenses:
        cat = e.get("category", "uncategorized")
        totals[cat] = totals.get(cat, 0.0) + e["amount"]
    print(f"{'Category':<15} {'Total':>10}")
    print("-" * 26)
    for cat, amt in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{cat:<15} {amt:>10.2f}")
    print("-" * 26)
    print(f"{'All':<15} {sum(totals.values()):>10.2f}")
    return 0


def export_csv(output_path="expenses.csv"):
    expenses = load_expenses()
    if not expenses:
        print("No expenses to export.")
        return 0
    try:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "date", "amount", "category", "note"])
            writer.writeheader()
            for e in sorted(expenses, key=lambda x: (x["date"], x["id"])):
                writer.writerow(e)
        print(f"Exported {len(expenses)} expense(s) to '{output_path}'.")
        return 0
    except OSError as err:
        print(f"Error exporting to CSV: {err}", file=sys.stderr)
        return 1


def build_parser():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("amount", type=float, help="Amount of the expense (positive number)")
    add_parser.add_argument("category", type=str, help="Category of the expense")
    add_parser.add_argument("note", type=str, nargs="?", default="", help="Optional note for the expense")
    add_parser.add_argument("--date", type=str, help="Date in YYYY-MM-DD format (default: today)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all expenses")
    list_parser.add_argument("--category", type=str, help="Filter by category")
    list_parser.add_argument("--month", type=str, help="Filter by month (YYYY-MM)")

    # Total command
    total_parser = subparsers.add_parser("total", help="Show total expenses")
    total_parser.add_argument("--category", type=str, help="Filter by category")
    total_parser.add_argument("--month", type=str, help="Filter by month (YYYY-MM)")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense by ID")
    delete_parser.add_argument("id", type=int, help="ID of the expense to delete")

    # Summary command
    subparsers.add_parser("summary", help="Show summary of expenses grouped by category")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export all expenses to a CSV file")
    export_parser.add_argument("-o", "--output", default="expenses.csv", help="Output file path (default: expenses.csv)")

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
        return list_expenses(args.category, args.month)
    elif args.command == "total":
        return total_expenses(args.category, args.month)
    elif args.command == "delete":
        return delete_expense(args.id)
    elif args.command == "summary":
        return summary()
    elif args.command == "export":
        return export_csv(args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
