from tkinter import *
import customtkinter
import ttkbootstrap as tb
import ttkbootstrap as ttk
from tkinter import messagebox
import sqlite3

root = customtkinter.CTk() # always place at beginning
root.title('Handcycle Converter')
root.iconbitmap('favicon.ico') # favicon for window
root.geometry()
style = ttk.Style('darkly')


customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green",
# "dark-blue"


#   Main Process -------->
def data_and_store(nickname_entry, duration_entry, date_entry, revs_slider,
                   min_h_slider, max_h_slider, revs_range_label, km_label, label_result):
    nickname = nickname_entry.get()
    duration = duration_entry.get()
    date = date_entry.entry.get()
    revs = revs_slider.get()
    min_h = min_h_slider.get()
    max_h = max_h_slider.get()

    # Validate input error message if not complete
    if not nickname or not duration or not revs:
        messagebox.showerror("Error", "Please complete all fields.")
        return

    try:
        revs = int(revs)
    except ValueError:
        messagebox.showerror("Error", "Handcycle revolutions must be a valid number.")
        return

    try:
        max_h = int(max_h_slider.get())
        if 0 <= max_h <= 85:
            label_result.configure(text=f"{max_h} Max Heart Rate = Tranquilisation State",
                                   text_color='red') # pink
        elif 87 <= max_h <= 102:
            label_result.configure(text=f"{max_h} Max Heart Rate = Stress Relieving State")  # blue

        elif 103 <= max_h <= 119:
            label_result.configure(text=f"{max_h} Max Heart Rate = Fat Burning State") # green

        elif 120 <= max_h <= 136:
            label_result.configure(text=f"{max_h} Max Heart Rate = Cardiopulmonary State") # yell

        elif 137 <= max_h <= 153:
            label_result.configure(text=f"{max_h} Max Heart Rate = Anaerobic State") # ornge

        elif 154 <= max_h <= 200:
            label_result.configure(text=f"{max_h} Max Heart Rate = Extremity State") # red
        else:
            label_result.configure(text="Max Heart Rate specified is out of defined range")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid integer")

    # Calculate kilometers from hand pedal revs
    kilometers = revs / 80 / 2  # there is 0.5Km to every 80 revs (1 min interval) on
    # average

    # Revs Range Label and KM Label
    revs_range_label.configure(text=str(revs))
    km_label.configure(text=f"{revs} Revolutions = {kilometers:.2f} km")

    print('Nickname: ', nickname, 'Duration: ', duration, 'Date: ', date)
    print('Revolutions: ', revs, 'Min Heart: ', min_h, 'Max Heart: ', max_h)
    print('Kilometers: ', kilometers)
    print('--------------------------------------------------------')

    # Create DB Table

    conn = sqlite3.connect('hcycle_data4.db')
    table_create_query = '''CREATE TABLE IF NOT EXISTS Student_Data
              (nickname TEXT, duration INTEGER, date TEXT, revs INTEGER, 
              min_h TEXT, max_h TEXT, kilometers INTEGER)
      '''
    conn.execute(table_create_query)

    # Insert Data
    data_insert_query = '''INSERT INTO Student_Data (nickname, duration, date, 
    revs, min_h, max_h, kilometers) VALUES (?,?,?,?,?,?,?)'''
    data_insert_tuple = (nickname, duration, date, revs, min_h, max_h, kilometers)

    cursor = conn.cursor()
    cursor.execute(data_insert_query, data_insert_tuple)
    conn.commit()
    conn.close()


#   OUTER_FRAME CONSTRUCTION---------------->
# Outside of frame dimensions
outer_frame = customtkinter.CTkFrame(root, corner_radius=0, border_width=0)
outer_frame.pack(padx=10, pady=5) # inside of frame
# dimensions



#   OUTER_FRAME CONTENT HERE---------------->

heading_label = Label(outer_frame, text='Gras Hand Cycle Converter',
                      justify=CENTER)

#   INNER_FRAME CONSTRUCTION---------------->
# Outside of frame dimensions
inner_frame0 = customtkinter.CTkFrame(outer_frame, corner_radius=0, border_width=0)
inner_frame0.grid(row=0, column=0, padx=10, pady=10) # inside of frame
# dimensions



#   INNER_FRAME CONTENT HERE---------------->


#  DATE FRAME FOR SELECTOR ------------->
def date_cal():
# BOOTSTRAP CALENDAR POPUP FOR DATE SELECTION
    date_label.config(text=f'{date_entry.entry.get()}', corner_radius=0)

date_frame = customtkinter.CTkFrame(inner_frame0, corner_radius=0,
                                    fg_color='transparent', border_width=0)
date_frame.grid(row=5, column=0, padx=0, pady=0) # inside of frame dimensions

date_entry = tb.DateEntry(inner_frame0, bootstyle='success')
date_entry.grid(row=6, column=0, padx=0, pady=0)

date_label = customtkinter.CTkLabel(date_frame, text='Date', corner_radius=0)
date_label.grid(row=8, column=0)

# saving user info

nickname_label = customtkinter.CTkLabel(inner_frame0, text='Nickname', corner_radius=0)
nickname_label.grid(row=0, column=0)
nickname_entry = customtkinter.CTkEntry(inner_frame0, corner_radius=0)
nickname_entry.grid(row=1, column=0)

duration_entry = customtkinter.CTkEntry(inner_frame0, corner_radius=0)
duration_entry.grid(row=3, column=0)
duration_label = customtkinter.CTkLabel(inner_frame0, text='Duration (mins)', corner_radius=0)
duration_label.grid(row=2, column=0)

for widget in inner_frame0.winfo_children():
    widget.grid_configure(padx=0, pady=5)

#   END INNER_FRAME CONTENT ---------------->


#   INNER_FRAME CONSTRUCTION---------------->


# Outside of frame dimensions
inner_frame1 = customtkinter.CTkFrame(outer_frame, corner_radius=0)
inner_frame1.grid(row=0, column=1, padx=10, pady=10) # inside of frame dimensions

#   INNER_FRAME CONTENT HERE---------------->

# ---- REVS FUNCTIONS
def revslide(value):
    revs_range.configure(text=int(value))

# Revs Title
revs_label = customtkinter.CTkLabel(inner_frame1, text='Revolutions')
revs_label.grid(row=4, column=0)
# Revs slider
revs_slider = customtkinter.CTkSlider(inner_frame1, from_=0, to=2000,
                                  command=revslide, orientation='vertical')
# Format
revs_slider.grid(row=5, column=0)
# Defines starting point
revs_slider.set(0)
# Revs gauge
revs_range = customtkinter.CTkLabel(inner_frame1, text='')
revs_range.grid(row=6, column=0, pady=0)

# Saving Heartrate Info

# MIN H FUNCTION
def minhslide(value):
    min_h_range.configure(text=int(value))

# MIN H Title
min_h_label = customtkinter.CTkLabel(inner_frame1, text='Heart Min')
min_h_label.grid(row=4, column=1)

# Minh slider
min_h_slider = customtkinter.CTkSlider(inner_frame1, from_=60, to=200,
                                      command=minhslide, orientation='vertical')
# Format
min_h_slider.grid(row=5, column=1)
# Defines starting point
min_h_slider.set(60)
# Min_h gauge
min_h_range = customtkinter.CTkLabel(inner_frame1, text='')
min_h_range.grid(row=6, column=1, pady=0)



# MAX H FUNCTION
def maxhslide(value):
    max_h_range.configure(text=int(value))

# MAX h Title
max_h_label = customtkinter.CTkLabel(inner_frame1, text='Heart Max')
max_h_label.grid(row=4, column=2)

# MAX H slider
max_h_slider = customtkinter.CTkSlider(inner_frame1, from_=60, to=200,
                                      command=maxhslide, orientation='vertical')
# Format
max_h_slider.grid(row=5, column=2)
# Defines starting point
max_h_slider.set(60)
# Min_h gauge
max_h_range = customtkinter.CTkLabel(inner_frame1, text='')
max_h_range.grid(row=6, column=2, pady=0)

for widget in inner_frame1.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Define revs_range_label
revs_range_label = customtkinter.CTkLabel(inner_frame1, text='')
revs_range_label.grid(row=6, column=0, pady=0)



#   END INNER_FRAME CONTENT ---------------->


#   INNER_FRAME CONSTRUCTION---------------->
# Outside of frame dimensions
inner_frame2 = customtkinter.CTkFrame(root)
inner_frame2.pack(padx=20, pady=10) # inside of frame dimensions

#   INNER_FRAME CONTENT HERE---------------->

# Button
button = customtkinter.CTkButton(inner_frame1, text='Submit Data',
                                 command=lambda: data_and_store(nickname_entry,
                                                                duration_entry,
                                                                date_entry, revs_slider,
                                                                min_h_slider, max_h_slider,
                                                                revs_range_label,
                                                                km_label, label_result))
button.grid(row=7, column=1, sticky='news', padx=10, pady=10)





# Onscreen KM converter

km_label = customtkinter.CTkLabel(inner_frame2, text='Conversion...')
km_label.grid(padx=50, pady=0)

# On screen max heart rate feedback
label_result = customtkinter.CTkLabel(inner_frame2, text="")
label_result.grid()






#   END INNER_FRAME CONTENT ---------------->




#   END OUTER_FRAME CONTENT ---------------->


root.mainloop()  # always place at very end of rest of code