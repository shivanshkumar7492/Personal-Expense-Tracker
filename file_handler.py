"""
file_handler.py
---------------
Handles reading and writing expense data to a JSON file.
Demonstrates file handling and exception handling.
"""

import json
import os
import shutil
from expense import Expense


class FileHandler:
    """Manages persistent storage of expenses in a JSON file."""

    def __init__(self, filepath: str = "expenses.json"):
        self.__filepath = filepath

    @property
    def filepath(self) -> str:
        return self.__filepath

    def save(self, expenses: list[Expense]) -> None:
        """Save the list of Expense objects to the JSON file.

        Creates a backup before writing to prevent data corruption.
        """
        backup_path = self.__filepath + ".bak"

        try:
            # create backup of existing file
            if os.path.exists(self.__filepath):
                shutil.copy2(self.__filepath, backup_path)

            data = [expense.to_dict() for expense in expenses]

            with open(self.__filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except PermissionError:
            print(f"  Error: Permission denied when writing to '{self.__filepath}'.")
        except OSError as e:
            print(f"  Error: Could not save data — {e}")
            # restore backup if write failed
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.__filepath)
                print("  Previous data has been restored from backup.")

    def load(self) -> list[Expense]:
        """Load expenses from the JSON file and return a list of Expense objects.

        Returns an empty list if the file doesn't exist or is empty.
        """
        if not os.path.exists(self.__filepath):
            return []

        try:
            with open(self.__filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)

            return [Expense.from_dict(item) for item in data]

        except json.JSONDecodeError:
            print(f"  Warning: '{self.__filepath}' contains invalid JSON. Starting fresh.")
            return []
        except KeyError as e:
            print(f"  Warning: Malformed data in file (missing key {e}). Starting fresh.")
            return []
        except PermissionError:
            print(f"  Error: Permission denied when reading '{self.__filepath}'.")
            return []
        except OSError as e:
            print(f"  Error: Could not read data — {e}")
            return []
