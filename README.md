# Expense Tracker CLI

A simple command-line application to track, manage, and report your expenses. This Python CLI app allows you to add, list, update, delete, filter, summarize, and export your expenses to JSON and CSV formats.

## Features

- **Add Expenses:** Record new expenses with category, description, and amount.
- **List Expenses:** View all recorded expenses.
- **Update Expenses:** Modify the description or amount of an existing expense.
- **Delete Expenses:** Remove an expense by its ID.
- **Filter Expenses:** Show expenses by category.
- **Summary:** Display total expenses or expenses for a specific month.
- **Export:** Export all expenses to a CSV file.
- **Generate Report:** Save a JSON report of all expenses.

## Usage

First, activate your virtual environment:

```sh
source bin/activate
```

Then run the CLI:

```sh
python main.py <command> [options]
```

### Commands

- **add**  
  Add a new expense.
  ```
  python main.py add -c <category> -d <description> -a <amount>
  ```

- **list**  
  List all expenses.
  ```
  python main.py list
  ```

- **update**  
  Update an expense by ID.
  ```
  python main.py update <id> [-d <description>] [-a <amount>]
  ```

- **delete**  
  Delete an expense by ID.
  ```
  python main.py delete <id>
  ```

- **filter**  
  Filter expenses by category.
  ```
  python main.py filter -c <category>
  ```

- **summary**  
  Show total expenses or expenses for a specific month.
  ```
  python main.py summary [--month <month_number>]
  ```

- **export**  
  Export expenses to a CSV file.
  ```
  python main.py export [-f <filename>]
  ```

## Data Storage

- Expenses are stored in `expenses.json` in the project directory.
- CSV exports are saved as `<filename>.csv`.

## Requirements

- Python 3.12+
- See `requeriments.txt` for dependencies.

## License

MIT License

---

Developed for personal finance tracking and learning purposes.