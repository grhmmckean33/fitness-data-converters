import tkinter as tk
import customtkinter
from tkinter import messagebox
import sqlite3

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green",
# "dark-blue"

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.iconbitmap('C:\\Users\\user\\Documents\\Python\\EEG\\cycle_icon.ico')
app.geometry("1000x500")


class RowingData:
    def __init__(self, name, duration, date, strokes, min_h, max_h):
        self.name = name
        self.duration = duration
        self.date = date
        self.strokes = strokes
        self.min_h = min_h
        self.max_h = max_h


    def calculate_kilometers(self):
        kilometers = self.strokes * 10 / 1000  # 10m per stroke
        return kilometers


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    def store_data(self, rowing_data):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS rowing_data6
                         (name TEXT, duration TEXT, date TEXT, strokes INTEGER, 
                         kilometers 
                         REAL, min_h INTEGER, max_h INTEGER)''')
            c.execute("INSERT INTO rowing_data VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (rowing_data.name, rowing_data.duration, rowing_data.date,
                       rowing_data.strokes, rowing_data.calculate_kilometers(),
                       rowing_data.min_h, rowing_data.max_h))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Data stored successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to store data: {str(e)}")

# MAIN PROCESS -------------------------->
def main():
    root = customtkinter.CTk()
    root.title("Rowing Stroke Converter")

    # Create labels and entry fields
    name_label = customtkinter.CTkLabel(root, text="Nickname ")
    name_label.grid(row=1, column=0, pady=0, padx=50)
    name_entry = customtkinter.CTkEntry(root)
    name_entry.grid(row=2, column=0, pady=0, padx=50)

    duration_label = customtkinter.CTkLabel(root, text="Duration ")
    duration_label.grid(row=1, column=1, pady=0, padx=10)
    duration_entry = customtkinter.CTkEntry(root)
    duration_entry.grid(row=2, column=1, pady=0, padx=10)
    duration_entry.insert(0, 'To nearest minute....')


    def on_entry_click(event):
        if duration_entry.get() == 'To nearest minute....':
            duration_entry.delete(0, tk.END)
            duration_entry.configure(fg_color='black')

    def on_focusout(event):
        if not duration_entry.get():
            duration_entry.insert(0, 'To nearest minute....')
            duration_entry.configure(fg_color='grey')

    duration_entry.bind('<FocusIn>', on_entry_click)
    duration_entry.bind('<FocusOut>', on_focusout)

    # ----------- DATE field

    date_label = customtkinter.CTkLabel(root, text="Date ")
    date_label.grid(row=1, column=2, pady=10, padx=10)
    date_entry = customtkinter.CTkEntry(root)
    date_entry.grid(row=2, column=2, pady=0, padx=10)
    date_entry.insert(0, 'dd/mm/yy')

    def on_entry_click(event):
        if date_entry.get() == 'dd/mm/yy':
            date_entry.delete(0, tk.END)
            date_entry.configure(fg_color='black')

    def on_focusout(event):
        if not date_entry.get():
            date_entry.insert(0, 'dd/mm/yy.')
            date_entry.configure(fg_color='grey')

    date_entry.bind('<FocusIn>', on_entry_click)
    date_entry.bind('<FocusOut>', on_focusout)

    # STROKES FUNCTION

    def strokeslide(value):
        strokes_range.configure(text=int(value))
    # STROKE LABEL
    strokes_label = customtkinter.CTkLabel(root, text="Rowing Strokes ")
    strokes_label.grid(row=5, column=0)
    # Stroke RANGE SLIDER
    strokes_entry = customtkinter.CTkSlider(root, from_=0, to=2000, command=strokeslide)
    strokes_entry.grid(row=6, column=0)
    strokes_entry.set(0)
    # SLIDER INTEGER GAUGE
    strokes_range = customtkinter.CTkLabel(root, text='')
    strokes_range.grid(row=7, column=0, pady=0)

    # MIN H FUNCTION
    def minhslide(value):
        min_h_range.configure(text=int(value))

    # MIN H Title
    min_h_label = customtkinter.CTkLabel(root, text='Heart minimum')
    min_h_label.grid(row=5, column=1)

    # Minh slider
    min_h_slider = customtkinter.CTkSlider(root, from_=60, to=200,
                                           command=minhslide)
    # Format
    min_h_slider.grid(row=6, column=1)
    # Defines starting point
    min_h_slider.set(60)
    # Min_h gauge
    min_h_range = customtkinter.CTkLabel(root, text='')
    min_h_range.grid(row=7, column=1, pady=0)

    # MAX H FUNCTION
    def maxhslide(value):
        max_h_range.configure(text=int(value))
    # MAX h Title
    max_h_label = customtkinter.CTkLabel(root, text='Heart maximum')
    max_h_label.grid(row=5, column=2)

    # MAX H slider
    max_h_slider = customtkinter.CTkSlider(root, from_=60, to=200,
                                           command=maxhslide)
    # Format
    max_h_slider.grid(row=6, column=2)
    # Defines starting point
    max_h_slider.set(60)
    # Min_h gauge
    max_h_range = customtkinter.CTkLabel(root, text='')
    max_h_range.grid(row=7, column=2, pady=0)

    for widget in root.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    db_connection = DatabaseConnection('rowing_data6.db')

    # Define revs_range_label
    stroke_range_label = customtkinter.CTkLabel(root, text='')
    stroke_range_label.grid(row=6, column=0, pady=0)

    calculate_button = customtkinter.CTkButton(root, text="Calculate & Store",
                                 command=lambda: calculate_and_store(name_entry,
                                        duration_entry, date_entry, strokes_entry,
                        min_h_slider, max_h_slider, stroke_range_label, km_label,
                                                                     db_connection))
    calculate_button.grid(row=8, column=1, sticky='news', padx=0, pady=10)


    # Onscreen KM converter
    km_frame = customtkinter.CTkLabel(root, text='')
    km_frame.grid(row=9, column=1, padx=0, pady=10)
    km_label = customtkinter.CTkLabel(km_frame, text='Converting please wait....')
    km_label.grid(row=9, column=1,  padx=0, pady=10)



    root.mainloop()


def calculate_and_store(name_entry, duration_entry, date_entry, strokes_entry,
                        min_h_slider, max_h_slider, stroke_range_label, km_label,
                        db_connection):
    name = name_entry.get()
    duration = duration_entry.get()
    date = date_entry.get()
    strokes = strokes_entry.get()
    min_h = min_h_slider.get()
    max_h = max_h_slider.get()

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
    kilometers = strokes * 10 / 1000  # there are 10m to every stroke on average

    # stroke Range Label and KM Label
    stroke_range_label.configure(text=str(strokes))
    km_label.configure(text=f"{strokes} Strokes = {kilometers:.2f} km")

    rowing_data = RowingData(name, duration, date, strokes, min_h, max_h)

    # Store data in the database
    db_connection.store_data(rowing_data)


if __name__ == "__main__":
    main()
