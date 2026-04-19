import tkinter as tk
from board_utils import easy_mode, medium_mode, hard_mode, clear_btn

def show_frame(frame):
    frame.tkraise()

# --- Root window setup ---
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("400x470")
root.configure(bg="lavender")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# --- Define Frames ---
menu_page   = tk.Frame(root, bg="lavender")
easy_page   = tk.Frame(root, bg="lightgreen")
medium_page = tk.Frame(root, bg="moccasin")
hard_page   = tk.Frame(root, bg="lightblue")   

for frame in (menu_page, easy_page, medium_page, hard_page):
    frame.grid(row=0, column=0, sticky="nsew")

# ── MENU PAGE ──────────────────────────────────────────────────────────────
tk.Label(menu_page, text="🎮 TIC-TAC-TOE 🎮", bg="lavender", fg="purple",
         font=("Arial", 16, "bold")).pack(pady=20)

tk.Button(menu_page, text="Easy Mode",   width=15, bg="white",
          command=lambda: show_frame(easy_page)).pack(pady=8)
tk.Button(menu_page, text="Medium Mode", width=15, bg="white",
          command=lambda: show_frame(medium_page)).pack(pady=8)
tk.Button(menu_page, text="Hard Mode",   width=15, bg="white",
          command=lambda: show_frame(hard_page)).pack(pady=8)

tk.Button(menu_page, text="Exit", width=10, bg="purple", fg="white",
          command=root.destroy).pack(pady=20)

# --- EASY PAGE ---
tk.Label(easy_page, text="Easy Mode 🟢", bg="lightgreen",
         font=("Arial", 14, "bold")).pack(pady=10)

# Frame to hold the grid
grid_frame = tk.Frame(easy_page, bg="lightgreen")
grid_frame.pack()

# Create 3x3 button grid
button_easy = []
for row in range(3):
    button_row = []
    for col in range(3):
        btn = tk.Button(grid_frame, text="", width=5, height=2, font=("Arial", 18))
        btn.config(command=lambda b=btn:easy_mode(b, button_easy))
        btn.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(btn)
    button_easy.append(button_row)

tk.Button(easy_page, text="Back to Menu", command=lambda: (show_frame(menu_page),clear_btn(button_easy))).pack(pady=10)

# --- MEDIUM PAGE ---
tk.Label(medium_page, text="Medium Mode 🔵", bg="moccasin",
         font=("Arial", 14, "bold")).pack(pady=20)


# Frame to hold the grid
grid_frame = tk.Frame(medium_page, bg="moccasin")
grid_frame.pack()

# Create 3x3 button grid
button_medium = []
for row in range(3):
    button_row = []
    for col in range(3):
        btn = tk.Button(grid_frame, text="", width=5, height=2, font=("Arial", 18))
        btn.config(command=lambda b=btn:medium_mode(b, button_medium))
        btn.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(btn)
    button_medium.append(button_row)

tk.Button(medium_page, text="Back to Menu", command=lambda: (show_frame(menu_page),clear_btn(button_medium))).pack()

# --- HARD PAGE ---
tk.Label(hard_page, text="Hard Mode 🔵 - Using Minimax", bg="lightblue",
         font=("Arial", 14, "bold")).pack(pady=20)

# Frame to hold the grid
grid_frame = tk.Frame(hard_page, bg="lightblue")
grid_frame.pack()

# Create 3x3 button grid
button_hard = []
for row in range(3):
    button_row = []
    for col in range(3):
        btn = tk.Button(grid_frame, text="", width=5, height=2, font=("Arial", 18))
        btn.config(command=lambda b=btn:hard_mode(b, button_hard))
        btn.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(btn)
    button_hard.append(button_row)

tk.Button(hard_page, text="Back to Menu", command=lambda: (show_frame(menu_page),clear_btn(button_hard))).pack()

# --- Show the main menu first ---
show_frame(menu_page)
root.mainloop()