import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Database setup function
def create_db():

    conn = sqlite3.connect('bmi_records.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    weight REAL,
                    height REAL,
                    bmi REAL,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

# Input validation function
def validate_input(weight, height):
   
    try:
        w = float(weight)
        h = float(height)
        if w <= 0 or w < 30 or w > 300:
            return False, "Weight must be between 30 and 300 kg."
        if h <= 0 or h < 100 or h > 250:
            return False, "Height must be between 100 and 250 cm."
        return True, ""
    except ValueError:
        return False, "Invalid input. Please enter numeric values for weight and height."

# BMI calculation function
def calculate_bmi(weight, height_cm):

    height_m = height_cm / 100.0
    return weight / (height_m ** 2)

# BMI categorization function
def categorize_bmi(bmi):

    if bmi < 18.5:
        return "Underweight", "blue"
    elif 18.5 <= bmi < 25:
        return "Normal", "green"
    elif 25 <= bmi < 30:
        return "Overweight", "orange"
    else:
        return "Obese", "red"

# Save record function
def save_record(username, weight, height, bmi):
  
    conn = sqlite3.connect('bmi_records.db')
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO records (username, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
              (username, weight, height, bmi, date))
    conn.commit()
    conn.close()

# Load history function
def load_history():

    conn = sqlite3.connect('bmi_records.db')
    c = conn.cursor()
    c.execute("SELECT username, date, weight, height, bmi FROM records ORDER BY date DESC")
    records = c.fetchall()
    conn.close()
    return records

# Load user history function
def load_user_history(username):
  
    conn = sqlite3.connect('bmi_records.db')
    c = conn.cursor()
    c.execute("SELECT date, weight, height, bmi FROM records WHERE username=? ORDER BY date DESC", (username,))
    records = c.fetchall()
    conn.close()
    return records

# Delete history function
def delete_history(username):
   
    conn = sqlite3.connect('bmi_records.db')
    c = conn.cursor()
    c.execute("DELETE FROM records WHERE username=?", (username,))
    conn.commit()
    conn.close()

# Show graph function
def show_graph(username):
   
    records = load_user_history(username)
    if not records:
        messagebox.showinfo("No Data", "No records found for this user.")
        return
    dates = [r[0] for r in records]
    bmis = [r[3] for r in records]
    plt.figure(figsize=(10, 5))
    plt.plot(dates, bmis, marker='o', linestyle='-')
    plt.title(f'BMI Trend for {username}')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.xticks(rotation=45)
    plt.grid(True)
    # Statistics
    min_bmi = min(bmis)
    max_bmi = max(bmis)
    avg_bmi = sum(bmis) / len(bmis)
    plt.text(0.02, 0.98, f'Min BMI: {min_bmi:.2f}\nMax BMI: {max_bmi:.2f}\nAvg BMI: {avg_bmi:.2f}',
             transform=plt.gca().transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.tight_layout()
    plt.show()

# GUI Class
class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("700x600")
        create_db()  # Initialize database
        self.setup_ui()

    def setup_ui(self):
    
        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(input_frame)
        self.username_entry.grid(row=0, column=1)
        tk.Label(input_frame, text="Weight (kg):").grid(row=1, column=0, sticky="e")
        self.weight_entry = tk.Entry(input_frame)
        self.weight_entry.grid(row=1, column=1)
        tk.Label(input_frame, text="Height (cm):").grid(row=2, column=0, sticky="e")
        self.height_entry = tk.Entry(input_frame)
        self.height_entry.grid(row=2, column=1)

        # Button Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Calculate BMI", command=self.calculate).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Save Record", command=self.save).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="View History", command=self.view_history).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Show Graph", command=self.graph).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Delete History", command=self.delete).grid(row=0, column=4, padx=5)

        # Result Label
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        # History Frame
        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(pady=10, fill="both", expand=True)
        self.history_tree = ttk.Treeview(self.history_frame, columns=("Username", "Date", "Weight", "Height", "BMI"), show="headings", height=10)
        self.history_tree.heading("Username", text="Username")
        self.history_tree.heading("Date", text="Date")
        self.history_tree.heading("Weight", text="Weight (kg)")
        self.history_tree.heading("Height", text="Height (cm)")
        self.history_tree.heading("BMI", text="BMI")
        self.history_tree.column("Username", width=100)
        self.history_tree.column("Date", width=150)
        self.history_tree.column("Weight", width=100)
        self.history_tree.column("Height", width=100)
        self.history_tree.column("BMI", width=100)
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def calculate(self):
   
        username = self.username_entry.get().strip()
        weight = self.weight_entry.get().strip()
        height = self.height_entry.get().strip()
        valid, msg = validate_input(weight, height)
        if not valid:
            messagebox.showerror("Invalid Input", msg)
            return
        w = float(weight)
        h = float(height)
        bmi = calculate_bmi(w, h)
        category, color = categorize_bmi(bmi)
        self.result_label.config(text=f"BMI: {bmi:.2f} - {category}", fg=color)

    def save(self):
    
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return
        weight = self.weight_entry.get().strip()
        height = self.height_entry.get().strip()
        valid, msg = validate_input(weight, height)
        if not valid:
            messagebox.showerror("Invalid Input", msg)
            return
        w = float(weight)
        h = float(height)
        bmi = calculate_bmi(w, h)
        save_record(username, w, h, bmi)
        messagebox.showinfo("Success", "Record saved successfully.")
        self.view_history()  # Refresh history

    def view_history(self):
  
        records = load_history()
        # Clear existing items
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)
        # Insert new records
        for record in records:
            self.history_tree.insert("", tk.END, values=record)

    def graph(self):
    
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return
        show_graph(username)

    def delete(self):
       
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete all history for '{username}'?"):
            delete_history(username)
            messagebox.showinfo("Success", "History deleted successfully.")
            self.view_history()  # Refresh history

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
