# 💰 Personal Expense Tracker

A command-line expense tracker built with **Python** and **Object-Oriented Programming** to manage daily expenses efficiently.

---

## Features

- **Add expenses** with amount, category, description, and date
- **View all expenses** in a formatted table sorted by date
- **Edit & delete** existing expenses by ID
- **Filter** by category, date range, or month
- **Search** expenses by keyword in descriptions
- **Category-wise summary** with percentage breakdown and visual bar chart
- **Monthly reports** for any year/month
- **Highlights** — view highest and lowest expenses at a glance
- **Full report** — complete overview of all spending
- **Persistent storage** — data saved to JSON and loaded automatically on startup
- **Data backup** — automatic backup before every save to prevent corruption

---

## Project Structure

```
Personal-Expense-Tracker/
│
├── main.py              # Entry point — CLI menu and user interaction
├── expense.py           # Expense class with encapsulation and validation
├── expense_manager.py   # Core logic — CRUD, filtering, calculations
├── file_handler.py      # JSON file persistence and exception handling
├── report.py            # Formatted reports and summaries
│
├── requirements.txt     # Dependencies (stdlib only)
├── .gitignore
└── README.md
```

---

## OOP Concepts Demonstrated

| Concept           | Where                                                                 |
|-------------------|-----------------------------------------------------------------------|
| **Encapsulation** | Private attributes with `@property` getters/setters in `Expense`     |
| **Composition**   | `ExpenseManager` uses `FileHandler`; `ReportGenerator` uses `ExpenseManager` |
| **Validation**    | Setter methods enforce positive amounts, valid categories, date format |
| **Serialization** | `to_dict()` / `from_dict()` class method for JSON conversion         |
| **Separation of Concerns** | Data model, business logic, persistence, and UI in separate modules |

---

## How to Run

### Prerequisites

- Python 3.10 or higher

### Steps

```bash
# Clone the repository
git clone https://github.com/shivanshkumar7492/Personal-Expense-Tracker.git
cd Personal-Expense-Tracker

# Run the tracker
python main.py
```

No external packages required — the project uses only the Python standard library.

---

## Usage

```
╔══════════════════════════════════════════════╗
║        PERSONAL EXPENSE TRACKER              ║
╠══════════════════════════════════════════════╣
║  1.  Add Expense                             ║
║  2.  View All Expenses                       ║
║  3.  Edit Expense                            ║
║  4.  Delete Expense                          ║
║  5.  Filter by Category                      ║
║  6.  Filter by Date Range                    ║
║  7.  Search by Keyword                       ║
║  8.  Category-wise Summary                   ║
║  9.  Monthly Report                          ║
║  10. Highlights (Highest / Lowest)           ║
║  11. Full Report                             ║
║  0.  Exit                                    ║
╚══════════════════════════════════════════════╝
```

### Example — Adding an Expense

```
── Add New Expense ──
  Amount (₹): 250
  Available categories:
    1. Food
    2. Transport
    3. Shopping
    ...
  Enter category number: 1
  Description: Lunch at office canteen
  Date (YYYY-MM-DD, leave blank for today):

  ✓ Expense added successfully!  →  [1]  2026-09-28  |  ₹250.00     |  Food             |  Lunch at office canteen
```

### Example — Category Summary

```
============================================================
  CATEGORY-WISE BREAKDOWN
============================================================
  Category         Amount    Share
  ------------------------------------
  Food            ₹  1200.00   48.0%  █████████
  Transport       ₹   800.00   32.0%  ██████
  Shopping        ₹   500.00   20.0%  ████
  ------------------------------------
  TOTAL           ₹  2500.00   100.0%
```

---

## Key Technical Details

- **Data storage**: Expenses are stored in `expenses.json` (auto-created on first run)
- **Backup**: A `.bak` file is created before every write operation
- **Exception handling**: Covers `FileNotFoundError`, `JSONDecodeError`, `ValueError`, `PermissionError`, and `OSError`
- **Input validation**: All user inputs are validated with retry loops — the program never crashes on bad input
- **Type hints**: Used throughout for readability and maintainability

---

## Built With

- Python 3.10+
- Standard library modules: `json`, `os`, `shutil`, `datetime`

---

## Author

**Shivansh Kumar** — [GitHub](https://github.com/shivanshkumar7492)
