import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime


class RowingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Rowing Stroke Converter")

        # Create labels and entry fields for user input
        self.name_label = tk.Label(master, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.date_label = tk.Label(master, text="Date:")
        self.date_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.date_entry = tk.Entry(master)
        self.date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.strokes_label = tk.Label(master, text="Rowing Strokes:")
        self.strokes_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.strokes_entry = tk.Entry(master)
        self.strokes_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Create a button to calculate and store the data
        self.calculate_button = tk.Button(master, text="Calculate & Store",
                                          command=self.calculate_and_store)
        self.calculate_button.grid(row=3, columnspan=2, padx=10, pady=10)

    def calculate_and_store(self):
        name = self.name_entry.get()
        date = self.date_entry.get()
        strokes = self.strokes_entry.get()

        # Validate input
        if not name or not date or not strokes:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            strokes = int(strokes)
        except ValueError:
            messagebox.showerror("Error", "Rowing strokes must be a valid number.")
            return

        # Calculate kilometers from rowing strokes
        kilometers = strokes * 0.001

        # Store data in a dictionary
        data = {
            "name": name,
            "date": date,
            "strokes": strokes,
            "kilometers": kilometers
        }

        # Save data to a JSON file
        filename = "rowing_data.json"
        try:
            with open(filename, "a") as f:
                json.dump(data, f)
                f.write(
                    '\n')  # Add a newline for readability when appending multiple records
            messagebox.showinfo("Success", "Data stored successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to store data: {str(e)}")


def main():
    root = tk.Tk()
    app = RowingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
