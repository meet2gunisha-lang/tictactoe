
import tkinter as tk
import random

# Function to switch pages
def show_frame(frame):
    frame.tkraise()  # Bring selected frame to the front

# --- Root window setup ---
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("400x400")
root.configure(bg="pink")

# Configure grid so all frames stack perfectly
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# --- Define Frames (pages) ---
menu_page = tk.Frame(root, bg="pink")
easy_page = tk.Frame(root, bg="lightgreen")
hard_page = tk.Frame(root, bg="lightblue")

# Place all pages in the same grid cell
for frame in (menu_page, easy_page, hard_page):
    frame.grid(row=0, column=0, sticky="nsew")
        

# --- MENU PAGE ---
tk.Label(menu_page, text="🎮 TIC-TAC-TOE 🎮", bg="pink", fg="red",
         font=("Arial", 16, "bold")).pack(pady=20)

tk.Button(menu_page, text="Easy Mode", width=15, bg="white",
          command=lambda: show_frame(easy_page)).pack(pady=10)

tk.Button(menu_page, text="Hard Mode", width=15, bg="white",
          command=lambda: show_frame(hard_page)).pack(pady=10)

tk.Button(menu_page, text="Exit", width=10, bg="red", fg="white",
          command=root.destroy).pack(pady=20)

# --- EASY PAGE ---
tk.Label(easy_page, text="Easy Mode 🟢", bg="lightgreen",
         font=("Arial", 14, "bold")).pack(pady=10)

#User pressed button gives X

def Replace_x(btn):
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        # flatten + filter for empty buttons
        empty_buttons = [b for row in buttons for b in row if b.cget("text") == ""]

        if empty_buttons:  # only if any are left
            ai_btn = random.choice(empty_buttons)
            ai_btn.config(text="O", state=tk.DISABLED)


# Frame to hold the grid
grid_frame = tk.Frame(easy_page, bg="lightgreen")
grid_frame.pack()

# Create 3x3 button grid
buttons = []
for row in range(3):
    button_row = []
    for col in range(3):
        btn = tk.Button(grid_frame, text="", width=5, height=2, font=("Arial", 18))
        btn.config(command=lambda b=btn:Replace_x(b))
        btn.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(btn)
    buttons.append(button_row)

# Back button
tk.Button(easy_page, text="Back to Menu", command=lambda: show_frame(menu_page)).pack(pady=10)




# --- HARD PAGE ---
tk.Label(hard_page, text="Hard Mode 🔵", bg="lightblue",
         font=("Arial", 14, "bold")).pack(pady=20)

# Frame to hold the grid
grid_frame = tk.Frame(hard_page, bg="lightblue")
grid_frame.pack()

# Create 3x3 button grid
button = []
for row in range(3):
    button_row = []
    for col in range(3):
        btn = tk.Button(grid_frame, text="", width=5, height=2, font=("Arial", 18),
                        command=lambda r=row, c=col: print(f"Clicked Hard: {r},{c}"))
        btn.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(btn)
    button.append(button_row)

tk.Button(hard_page, text="Back to Menu", command=lambda: show_frame(menu_page)).pack()

# --- Show the main menu first ---
show_frame(menu_page)

# --- Start the app ---
root.mainloop()
