
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
from datetime import datetime
import matplotlib.pyplot as plt
import csv
import threading
import requests
import json

# Firebase Admin SDK for database interaction
import firebase_admin
from firebase_admin import credentials, firestore

class ExpenseTrackerApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Smart Expense Tracker Bot")
        self.root.geometry("650x700")
        self.root.resizable(False, False)

        # --- Style Configuration ---
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.configure_styles()

        # --- Firebase Initialization ---
        self.db = self.initialize_firebase()
        if not self.db:
            messagebox.showerror("Firebase Error", "Could not initialize Firebase. Please check 'firebase_key.json'.")
            self.root.destroy()
            return
            
        # --- Variables ---
        # Your Gemini API key is now hard-coded here.
        self.gemini_api_key = "Add your gemini key here"

        # --- UI Creation ---
        self.create_widgets()

    def configure_styles(self):
        """Configure custom styles for ttk widgets for a professional look."""
        self.root.configure(bg="#F0F2F5")
        # Frame styles
        self.style.configure('TFrame', background='#F0F2F5')
        self.style.configure('Header.TFrame', background='#FFFFFF', borderwidth=1, relief='solid')
        self.style.configure('Input.TFrame', background='#FFFFFF')
        # Label styles
        self.style.configure('TLabel', background='#FFFFFF', font=('Segoe UI', 10), foreground='#333333')
        self.style.configure('Header.TLabel', background='#F0F2F5', font=('Segoe UI', 18, 'bold'), foreground='#0052CC')
        self.style.configure('Footer.TLabel', background='#F0F2F5', font=('Segoe UI', 9), foreground='#555555')
        # Button styles
        self.style.configure('TButton', font=('Segoe UI', 11, 'bold'), padding=10, borderwidth=0)
        self.style.map('TButton',
                       foreground=[('active', '#FFFFFF')],
                       background=[('active', '#0041A3')])
        self.style.configure('Add.TButton', foreground='#FFFFFF', background='#28a745')
        self.style.configure('Chart.TButton', foreground='#FFFFFF', background='#007bff')
        self.style.configure('Budget.TButton', foreground='#FFFFFF', background='#ffc107')
        self.style.configure('Export.TButton', foreground='#FFFFFF', background='#6f42c1')
        self.style.configure('AI.TButton', foreground='#FFFFFF', background='#17a2b8')
        # Entry style
        self.style.configure('TEntry', font=('Segoe UI', 10), padding=5)


    def initialize_firebase(self):
        """Initializes the Firebase Admin SDK and returns a Firestore client instance."""
        try:
            cred = credentials.Certificate("firebase_key.json")
            firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            return None

    def create_widgets(self):
        """Creates and places all the widgets in the main window."""
        # --- Header ---
        header_label = ttk.Label(self.root, text="Smart Expense Tracker Bot", style='Header.TLabel')
        header_label.pack(pady=(15, 10))

        # --- Main Frame ---
        main_frame = ttk.Frame(self.root, padding=(20, 10), style='TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # --- Input Section ---
        input_labelframe = ttk.LabelFrame(main_frame, text="Log Your Expenses", padding=(15, 10))
        input_labelframe.pack(fill='x', pady=(0, 20))

        # Grid configuration for alignment
        input_labelframe.columnconfigure(1, weight=1)

        # Username
        ttk.Label(input_labelframe, text="Username:").grid(row=0, column=0, padx=5, pady=8, sticky='w')
        self.username_entry = ttk.Entry(input_labelframe, width=35)
        self.username_entry.grid(row=0, column=1, padx=5, pady=8, sticky='ew')
        
        # Category
        ttk.Label(input_labelframe, text="Category:").grid(row=1, column=0, padx=5, pady=8, sticky='w')
        self.category_entry = ttk.Entry(input_labelframe, width=35)
        self.category_entry.grid(row=1, column=1, padx=5, pady=8, sticky='ew')
        
        # Amount
        ttk.Label(input_labelframe, text="Amount ($):").grid(row=2, column=0, padx=5, pady=8, sticky='w')
        self.amount_entry = ttk.Entry(input_labelframe, width=35)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=8, sticky='ew')

        # Date
        ttk.Label(input_labelframe, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=8, sticky='w')
        self.date_entry = ttk.Entry(input_labelframe, width=35)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=3, column=1, padx=5, pady=8, sticky='ew')
        
        # Budget
        ttk.Label(input_labelframe, text="Monthly Budget ($):").grid(row=4, column=0, padx=5, pady=8, sticky='w')
        self.budget_entry = ttk.Entry(input_labelframe, width=35)
        self.budget_entry.insert(0, "1000")
        self.budget_entry.grid(row=4, column=1, padx=5, pady=8, sticky='ew')

        # --- Action Buttons ---
        actions_frame = ttk.Frame(main_frame, style='TFrame')
        actions_frame.pack(fill='x', pady=10)

        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)
        
        btn_add = ttk.Button(actions_frame, text="Add Expense", command=self.add_expense, style='Add.TButton')
        btn_add.grid(row=0, column=0, columnspan=2, pady=5, sticky='ew')
        
        btn_summary = ttk.Button(actions_frame, text="Show Monthly Chart", command=self.show_summary_chart, style='Chart.TButton')
        btn_summary.grid(row=1, column=0, pady=5, padx=(0, 5), sticky='ew')
        
        btn_budget = ttk.Button(actions_frame, text="Check Budget Status", command=self.check_budget_alert, style='Budget.TButton')
        btn_budget.grid(row=1, column=1, pady=5, padx=(5, 0), sticky='ew')
        
        btn_export = ttk.Button(actions_frame, text="Export to CSV", command=self.export_to_csv, style='Export.TButton')
        btn_export.grid(row=2, column=0, pady=5, padx=(0, 5), sticky='ew')
        
        btn_ai = ttk.Button(actions_frame, text="Get AI Savings Coach", command=self.get_ai_suggestions, style='AI.TButton')
        btn_ai.grid(row=2, column=1, pady=5, padx=(5, 0), sticky='ew')
        
        # --- Footer ---
        footer_label = ttk.Label(self.root, text="💡 Track smarter, spend wiser with AI!", style='Footer.TLabel')
        footer_label.pack(side="bottom", pady=10)

    # -----------------------------
    # Core Functions
    # -----------------------------

    def get_username(self):
        """Retrieves and validates the username from the entry field."""
        user = self.username_entry.get().strip()
        if not user:
            messagebox.showerror("Error", "Username is required to proceed.")
            return None
        return user

    def add_expense(self):
        """Adds a new expense record to Firestore."""
        user = self.get_username()
        if not user: return

        try:
            category = self.category_entry.get().strip()
            amount = float(self.amount_entry.get().strip())
            date = self.date_entry.get().strip()

            if not category or not date:
                messagebox.showerror("Error", "Please fill in all expense fields.")
                return

            self.db.collection("users").document(user).collection("expenses").add({
                "category": category,
                "amount": amount,
                "date": date
            })

            messagebox.showinfo("Success ✅", f"Added ${amount:.2f} under {category}.")
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the amount.")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def get_monthly_expenses(self, user):
        """Fetches and returns all expenses for the current month for a given user."""
        current_month = datetime.now().strftime("%Y-%m")
        expenses_ref = self.db.collection("users").document(user).collection("expenses")
        query = expenses_ref.where("date", ">=", current_month).where("date", "<", current_month + "-32")
        
        docs = query.stream()
        return [doc.to_dict() for doc in docs]

    def check_budget_alert(self):
        """Checks current spending against the budget and shows an alert."""
        user = self.get_username()
        if not user: return
        
        try:
            budget = float(self.budget_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid budget amount.")
            return
            
        expenses = self.get_monthly_expenses(user)
        total_spent = sum(e["amount"] for e in expenses)

        if total_spent > budget:
            messagebox.showerror("🚨 Budget Exceeded", f"You have exceeded your budget!\nTotal Spent: ${total_spent:.2f} / ${budget:.2f}")
        elif total_spent > 0.9 * budget:
            messagebox.showwarning("⚠️ Budget Warning", f"You are close to your limit!\nSpent: ${total_spent:.2f} / ${budget:.2f}")
        else:
            messagebox.showinfo("✅ Budget OK", f"You are within your budget.\nSpent: ${total_spent:.2f} / ${budget:.2f}")

    def show_summary_chart(self):
        """Generates and displays a pie chart of monthly expenses."""
        user = self.get_username()
        if not user: return

        expenses = self.get_monthly_expenses(user)
        summary = {}
        for e in expenses:
            cat = e["category"]
            summary[cat] = summary.get(cat, 0) + e["amount"]

        if not summary:
            messagebox.showinfo("Info", "No expenses found for the current month.")
            return

        plt.style.use('seaborn-v0_8-pastel')
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(summary.values(), labels=summary.keys(), autopct='%1.1f%%', startangle=140, pctdistance=0.85)
        
        # Draw a circle at the center to make it a donut chart
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)
        
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(f"{user}'s Monthly Expense Breakdown", pad=20)
        plt.tight_layout()
        plt.show()

    def export_to_csv(self):
        """Exports all user expenses to a CSV file."""
        user = self.get_username()
        if not user: return

        docs = self.db.collection("users").document(user).collection("expenses").stream()
        data = [e.to_dict() for e in docs]

        if not data:
            messagebox.showinfo("Info", "No expenses to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile=f"{user}_expenses_{datetime.now().strftime('%Y-%m-%d')}.csv"
        )
        if not file_path: return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["category", "amount", "date"])
                writer.writeheader()
                writer.writerows(data)
            messagebox.showinfo("Success ✅", f"Data exported successfully to {file_path}")
        except IOError as e:
            messagebox.showerror("Export Error", f"Could not save the file: {e}")

    # -----------------------------
    # Gemini API Integration
    # -----------------------------
    
    def get_ai_suggestions(self):
        """Main function to trigger the AI suggestion process."""
        user = self.get_username()
        if not user: return
        
        if not self.gemini_api_key:
            messagebox.showerror("API Key Error", "Gemini API key is not set in the code.")
            return

        # Show a loading message and run API call in a separate thread
        self.show_loading_window()
        
        # Start the API call in a new thread to avoid freezing the UI
        threading.Thread(target=self.fetch_and_display_suggestions, args=(user,), daemon=True).start()

    def fetch_and_display_suggestions(self, user):
        """Fetches data, calls Gemini API, and updates the UI with the response."""
        try:
            expenses = self.get_monthly_expenses(user)
            budget = float(self.budget_entry.get().strip())
    
            if not expenses:
                self.root.after(0, lambda: messagebox.showinfo("No Data", "Not enough expense data for this month to generate suggestions."))
                return
    
            prompt = self.create_gemini_prompt(expenses, budget)
            response = self.call_gemini_api(prompt)
            
            # Use `root.after` to schedule the UI update on the main thread
            self.root.after(0, self.display_suggestions, response)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {e}"))
        finally:
            # Ensure the loading window is always closed
            self.root.after(0, self.hide_loading_window)

    def create_gemini_prompt(self, expenses, budget):
        """Formats the expense data into a detailed prompt for the Gemini API."""
        expense_list = "\n".join([f"- Category: {e['category']}, Amount: ${e['amount']:.2f}" for e in expenses])
        total_spent = sum(e["amount"] for e in expenses)

        prompt = (
            "You are a friendly and helpful financial advisor. Analyze the following expense data "
            "for a user and provide practical, personalized money-saving suggestions. Be encouraging and clear.\n\n"
            f"User's Monthly Budget: ${budget:.2f}\n"
            f"Total Spent This Month: ${total_spent:.2f}\n\n"
            "Monthly Expenses:\n"
            f"{expense_list}\n\n"
            "Based on this data, please provide:\n"
            "1. A brief, encouraging summary of their spending habits.\n"
            "2. Identify the top 2-3 spending categories.\n"
            "3. Offer at least 3 actionable and specific tips to help them save money in those categories.\n"
            "Format the response clearly with headings."
        )
        return prompt

    def call_gemini_api(self, prompt):
        """Sends the prompt to the Gemini API and returns the text response."""
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={self.gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=30)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            result = response.json()
            
            # Safely extract text from the response
            candidate = result.get("candidates", [{}])[0]
            content = candidate.get("content", {})
            parts = content.get("parts", [{}])
            text = parts[0].get("text", "Sorry, I couldn't generate a response. Please try again.")
            return text
            
        except requests.exceptions.RequestException as e:
            return f"API Request Failed: {e}"
        except (KeyError, IndexError):
            return "Error: Received an invalid response format from the API."

    def display_suggestions(self, suggestions):
        """Displays the AI-generated suggestions in a new, scrollable window."""
        suggestion_window = tk.Toplevel(self.root)
        suggestion_window.title("AI Savings Coach")
        suggestion_window.geometry("500x400")
        suggestion_window.configure(bg="#F0F2F5")

        text_area = scrolledtext.ScrolledText(suggestion_window, wrap=tk.WORD, font=("Segoe UI", 10), bg="#FFFFFF", relief="solid", bd=1)
        text_area.pack(expand=True, fill='both', padx=15, pady=15)
        text_area.insert(tk.INSERT, suggestions)
        text_area.config(state='disabled') # Make it read-only
        
        close_button = ttk.Button(suggestion_window, text="Close", command=suggestion_window.destroy)
        close_button.pack(pady=(0, 10))

    def show_loading_window(self):
        """Shows a simple 'Loading...' Toplevel window."""
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("Loading")
        self.loading_window.geometry("200x80")
        self.loading_window.transient(self.root) # Keep it on top
        self.loading_window.grab_set() # Modal
        
        ttk.Label(self.loading_window, text="Analyzing your expenses...", font=("Segoe UI", 10)).pack(pady=10)
        progress = ttk.Progressbar(self.loading_window, mode='indeterminate')
        progress.pack(pady=5, padx=10, fill='x')
        progress.start(10)
    
    def hide_loading_window(self):
        """Hides the loading window if it exists."""
        if hasattr(self, 'loading_window') and self.loading_window.winfo_exists():
            self.loading_window.destroy()

# -----------------------------
# Main Execution Block
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

