"""
report.py
---------
Generates formatted text reports and summaries from expense data.
"""

from expense_manager import ExpenseManager


class ReportGenerator:
    """Produces formatted reports from an ExpenseManager instance."""

    def __init__(self, manager: ExpenseManager):
        self.__manager = manager

    # ---- helpers -------------------------------------------------------

    @staticmethod
    def _header(title: str) -> str:
        """Return a formatted section header."""
        line = "=" * 60
        return f"\n{line}\n  {title}\n{line}"

    @staticmethod
    def _format_table(expenses) -> str:
        """Format a list of expenses as a table string."""
        if not expenses:
            return "  No expenses found.\n"

        header = (
            f"  {'ID':<5} {'Date':<12} {'Amount':>10}   "
            f"{'Category':<15} {'Description'}"
        )
        separator = "  " + "-" * 65
        rows = []
        for e in expenses:
            rows.append(
                f"  {e.id:<5} {e.date:<12} ₹{e.amount:>9.2f}   "
                f"{e.category:<15} {e.description}"
            )
        return "\n".join([header, separator] + rows) + "\n"

    # ---- reports -------------------------------------------------------

    def full_report(self) -> str:
        """Generate a complete summary of all expenses."""
        expenses = self.__manager.get_all_expenses()
        lines = [self._header("FULL EXPENSE REPORT")]
        lines.append(f"  Total expenses recorded : {self.__manager.count}")
        lines.append(f"  Grand total             : ₹{self.__manager.total_expenses():.2f}\n")
        lines.append(self._format_table(expenses))
        return "\n".join(lines)

    def category_report(self) -> str:
        """Show spending broken down by category."""
        totals = self.__manager.total_by_category()
        lines = [self._header("CATEGORY-WISE BREAKDOWN")]

        if not totals:
            lines.append("  No expenses recorded yet.\n")
            return "\n".join(lines)

        grand_total = self.__manager.total_expenses()
        lines.append(f"  {'Category':<15} {'Amount':>10}   {'Share':>6}")
        lines.append("  " + "-" * 36)

        for cat, amount in totals.items():
            pct = (amount / grand_total * 100) if grand_total else 0
            bar = "█" * int(pct / 5)  # simple bar chart
            lines.append(f"  {cat:<15} ₹{amount:>9.2f}   {pct:>5.1f}%  {bar}")

        lines.append("  " + "-" * 36)
        lines.append(f"  {'TOTAL':<15} ₹{grand_total:>9.2f}   100.0%\n")
        return "\n".join(lines)

    def monthly_report(self, year: int, month: int) -> str:
        """Generate a report for a specific month."""
        expenses = self.__manager.filter_by_month(year, month)
        total = self.__manager.monthly_total(year, month)
        month_name = f"{year}-{month:02d}"

        lines = [self._header(f"MONTHLY REPORT — {month_name}")]
        lines.append(f"  Expenses this month : {len(expenses)}")
        lines.append(f"  Monthly total       : ₹{total:.2f}\n")
        lines.append(self._format_table(expenses))
        return "\n".join(lines)

    def highlights(self) -> str:
        """Show highest and lowest expenses."""
        lines = [self._header("HIGHLIGHTS")]
        high = self.__manager.highest_expense()
        low = self.__manager.lowest_expense()

        if high:
            lines.append(f"  Highest : ₹{high.amount:.2f} — {high.description} "
                         f"({high.category}, {high.date})")
        if low:
            lines.append(f"  Lowest  : ₹{low.amount:.2f} — {low.description} "
                         f"({low.category}, {low.date})")
        if not high:
            lines.append("  No expenses recorded yet.")

        lines.append("")
        return "\n".join(lines)
