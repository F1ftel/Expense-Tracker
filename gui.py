# gui.py
# Expense Tracker - Simple GUI Application
# Maksims Selkovskis ms24100, Raimonds Silinevics rs24085

import customtkinter as ctk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

from tracker import ExpenseTracker
from analytics import ExpenseAnalytics

class ExpenseTrackerGUI:
    CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Healthcare", "Education", "Travel", "Other"]
    
    def __init__(self):
        ctk.set_appearance_mode("light")
        self.tracker = ExpenseTracker("data/expenses.csv")
        self.analytics = ExpenseAnalytics(self.tracker)
        
        self.root = ctk.CTk()
        self.root.title("Expense Tracker")
        
        self.root.state('zoomed')
        
        self._build_ui()
    
    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self.root, fg_color="white")
        header.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(header, text="Expense Tracker", font=ctk.CTkFont(size=28, weight="bold")).pack(side="left", padx=20)
        ctk.CTkButton(header, text="Add Expense", command=self._add_expense, fg_color="#2ecc71", hover_color="#27ae60", width=150, height=35).pack(side="right", padx=20)
        
        # Tabs
        tabs = ctk.CTkTabview(self.root, fg_color="white")
        tabs.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.expenses_tab = tabs.add("All Expenses")
        self.analytics_tab = tabs.add("Analytics")
        
        self._setup_expenses_tab()
        self._setup_analytics_tab()
    
    def _setup_expenses_tab(self):
        container = ctk.CTkFrame(self.expenses_tab, fg_color="white")
        container.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Header
        header = ctk.CTkFrame(container, fg_color="white")
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header, text="All Expenses", font=ctk.CTkFont(size=24, weight="bold")).pack(side="left", padx=10)
        
        # Table
        table_frame = ctk.CTkFrame(container, fg_color="white")
        table_frame.pack(fill="both", expand=True)
        
        # Table header
        self._create_table_header(table_frame)
        
        # Scrollable content
        self.expenses_scroll = ctk.CTkScrollableFrame(table_frame, fg_color="white")
        self.expenses_scroll.pack(fill="both", expand=True)
        self._refresh_expenses()
    
    def _create_table_header(self, parent):
        header_row = ctk.CTkFrame(parent, fg_color="#f0f0f0", height=40)
        header_row.pack(fill="x")
        header_row.pack_propagate(False)
        
        for text, width in [("Date", 150), ("Category", 150), ("Amount", 120), ("Description", 300)]:
            ctk.CTkLabel(header_row, text=text, width=width, font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(side="left", padx=20)
        
        ctk.CTkLabel(header_row, text="Actions", width=100, font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(side="right", padx=20)
    
    def _refresh_expenses(self):
        for widget in self.expenses_scroll.winfo_children():
            widget.destroy()
        
        expenses = self.tracker.get_all_expenses()
        if expenses.empty:
            ctk.CTkLabel(self.expenses_scroll, text="No expenses. Add your first expense!", text_color="gray", font=ctk.CTkFont(size=14)).pack(pady=30)
            return
        
        expenses = expenses.sort_values("date", ascending=False).reset_index(drop=True)
        
        for _, row in expenses.iterrows():
            self._create_expense_row(row)
    
    def _create_expense_row(self, row):
        row_frame = ctk.CTkFrame(self.expenses_scroll, fg_color="white", height=45)
        row_frame.pack(fill="x", pady=1)
        row_frame.pack_propagate(False)
        
        date_str = row["date"].strftime("%Y-%m-%d") if pd.notna(row["date"]) else ""
        amount_str = f"{row['amount']:.2f} EUR"
        desc = row["description"] if pd.notna(row["description"]) and row["description"] else "-"
        
        # Truncate description if too long
        if len(desc) > 50:
            desc = desc[:47] + "..."
        
        for text, width in [(date_str, 150), (row["category"], 150), (amount_str, 120), (desc, 300)]:
            ctk.CTkLabel(row_frame, text=text, width=width, anchor="w", font=ctk.CTkFont(size=12)).pack(side="left", padx=20)
        
        # Check if ID exists (not None), don't use truthiness check since ID can be 0
        if "id" in row and pd.notna(row["id"]):
            expense_id = int(row["id"])
            ctk.CTkButton(row_frame, text="Delete", command=lambda eid=expense_id: self._delete_expense(eid), fg_color="#e74c3c", hover_color="#c0392b", width=100, height=32, font=ctk.CTkFont(size=11)).pack(side="right", padx=20)
    
    def _delete_expense(self, expense_id):
        if self.tracker.delete_expense(expense_id):
            self._refresh_expenses()
            self._refresh_analytics()
    
    def _add_expense(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Expense")
        dialog.geometry("500x550")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 250
        y = (dialog.winfo_screenheight() // 2) - 275
        dialog.geometry(f"500x550+{x}+{y}")
        
        form = ctk.CTkFrame(dialog, fg_color="white")
        form.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(form, text="Add New Expense", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(10, 25))
        
        # Create form fields
        date_entry = self._create_form_field(form, "Date (YYYY-MM-DD):", ctk.CTkEntry)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        category_dropdown = self._create_form_field(form, "Category:", ctk.CTkComboBox, values=self.CATEGORIES, state="readonly")
        category_dropdown.set(self.CATEGORIES[0])
        
        amount_entry = self._create_form_field(form, "Amount:", ctk.CTkEntry)
        desc_entry = self._create_form_field(form, "Description (optional):", ctk.CTkEntry)
        
        status = ctk.CTkLabel(form, text="", text_color="green")
        status.pack(pady=10)
        
        def submit():
            try:
                date = date_entry.get().strip()
                category = category_dropdown.get().strip()
                amount = float(amount_entry.get().strip())
                description = desc_entry.get().strip()
                
                if not date or not category or amount <= 0:
                    raise ValueError("Invalid input")
                
                datetime.strptime(date, "%Y-%m-%d")
                self.tracker.add_expense(date, category, amount, description or "")
                status.configure(text="Added successfully!", text_color="green")
                dialog.after(1000, dialog.destroy)
                self._refresh_expenses()
                self._refresh_analytics()
            except Exception as e:
                status.configure(text=f"Error: {str(e)}", text_color="red")
        
        # Buttons
        buttons = ctk.CTkFrame(form, fg_color="white")
        buttons.pack(pady=10)
        ctk.CTkButton(buttons, text="Add", command=submit, fg_color="#2ecc71", hover_color="#27ae60", width=150, height=40).pack(side="left", padx=10)
        ctk.CTkButton(buttons, text="Cancel", command=dialog.destroy, fg_color="#95a5a6", hover_color="#7f8c8d", width=150, height=40).pack(side="left", padx=10)
    
    def _create_form_field(self, parent, label_text, widget_class, **kwargs):
        ctk.CTkLabel(parent, text=label_text).pack(anchor="w", padx=20, pady=(0, 5))
        widget = widget_class(parent, width=400, height=35, **kwargs)
        widget.pack(padx=20, pady=(0, 15))
        return widget
    
    def _setup_analytics_tab(self):
        container = ctk.CTkFrame(self.analytics_tab, fg_color="white")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(container, text="Expense Analytics", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(10, 20))
        
        # Stats
        self._create_stats_section(container)
        
        # Charts
        chart_tabs = ctk.CTkTabview(container, fg_color="white")
        chart_tabs.pack(fill="both", expand=True)
        
        self.chart_tabs = {
            "pie": chart_tabs.add("By Category"),
            "time": chart_tabs.add("Over Time"),
            "monthly": chart_tabs.add("Monthly")
        }
        
        for chart_type, tab in self.chart_tabs.items():
            self._create_chart(chart_type, tab)
    
    def _create_stats_section(self, parent):
        stats_frame = ctk.CTkFrame(parent, fg_color="#f0f0f0")
        stats_frame.pack(fill="x", pady=(0, 20))
        
        expenses = self.tracker.get_all_expenses()
        total = self.analytics.total_expenses()
        avg_daily = self.analytics.average_daily_expenses()
        num_cats = expenses["category"].nunique() if not expenses.empty else 0
        
        stats_inner = ctk.CTkFrame(stats_frame, fg_color="#f0f0f0")
        stats_inner.pack(expand=True, pady=20)
        
        self.stats_labels = {}
        stats = [("Total Expenses", f"{total:.2f} EUR", "total"), ("Average Daily", f"{avg_daily:.2f} EUR", "avg"), ("Categories", str(num_cats), "cats")]
        
        for col, (label, value, key) in enumerate(stats):
            ctk.CTkLabel(stats_inner, text=label, text_color="gray", fg_color="#f0f0f0").grid(row=0, column=col, padx=40, pady=5)
            label_widget = ctk.CTkLabel(stats_inner, text=value, font=ctk.CTkFont(size=24, weight="bold"), fg_color="#f0f0f0")
            label_widget.grid(row=1, column=col, padx=40, pady=5)
            self.stats_labels[key] = label_widget
    
    def _create_chart(self, chart_type, parent):
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        df = self.tracker.get_all_expenses()
        
        if df.empty:
            ax.text(0.5, 0.5, "No data available", ha="center", va="center", fontsize=14)
            ax.axis('off')
        elif chart_type == "pie":
            self._create_pie_chart(ax)
        elif chart_type == "time":
            self._create_time_chart(ax, fig, df)
        elif chart_type == "monthly":
            self._create_monthly_chart(ax, fig)
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def _create_pie_chart(self, ax):
        by_cat = self.analytics.expenses_by_category()
        if not by_cat.empty:
            wedges, _, autotexts = ax.pie(by_cat.values, labels=None, autopct=lambda p: f'{p:.1f}%' if p > 3 else '', startangle=90, pctdistance=0.75)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
            labels = [f"{c}: {v:.2f} EUR" for c, v in zip(by_cat.index, by_cat.values)]
            ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
            ax.set_title("Expenses by Category", fontsize=14, fontweight="bold", pad=20)
    
    def _create_time_chart(self, ax, fig, df):
        df["date"] = pd.to_datetime(df["date"])
        daily = df.groupby(df["date"].dt.date)["amount"].sum()
        if not daily.empty:
            ax.plot(daily.index, daily.values, marker='o', linewidth=2, markersize=5, color='#3498db')
            ax.set_title("Expenses Over Time", fontsize=14, fontweight="bold", pad=20)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Amount (EUR)", fontsize=12)
            ax.grid(True, alpha=0.3)
            fig.autofmt_xdate()
    
    def _create_monthly_chart(self, ax, fig):
        monthly = self.analytics.monthly_totals()
        if not monthly.empty:
            ax.bar(range(len(monthly)), monthly.values, color='#3498db', alpha=0.7)
            ax.set_title("Monthly Totals", fontsize=14, fontweight="bold", pad=20)
            ax.set_xlabel("Month", fontsize=12)
            ax.set_ylabel("Amount (EUR)", fontsize=12)
            ax.set_xticks(range(len(monthly)))
            ax.set_xticklabels([str(p) for p in monthly.index], rotation=45, ha='right', fontsize=10)
            ax.grid(True, alpha=0.3, axis='y')
            fig.tight_layout()
    
    def _refresh_analytics(self):
        expenses = self.tracker.get_all_expenses()
        self.stats_labels["total"].configure(text=f"{self.analytics.total_expenses():.2f} EUR")
        self.stats_labels["avg"].configure(text=f"{self.analytics.average_daily_expenses():.2f} EUR")
        self.stats_labels["cats"].configure(text=str(expenses["category"].nunique() if not expenses.empty else 0))
        
        for chart_type, tab in self.chart_tabs.items():
            for widget in tab.winfo_children():
                widget.destroy()
            self._create_chart(chart_type, tab)
    
    def run(self):
        self.root.mainloop()


def main():
    app = ExpenseTrackerGUI()
    app.run()


if __name__ == "__main__":
    main()