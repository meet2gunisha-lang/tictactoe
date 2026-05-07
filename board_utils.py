import tkinter as tk
from board_utils import easy_mode, medium_mode, hard_mode, clear_btn
import random
from tkinter import messagebox
import json
import os
DB_FILE="stats.json"
#databse stuff
def load_stats():

    if not os.path.exists(DB_FILE):

        stats = {
            "player_wins": 0,
            "computer_wins": 0,
            "draws": 0,
            "games_played": 0
        }

        with open(DB_FILE, "w") as file:
            json.dump(stats, file)

        return stats

    with open(DB_FILE, "r") as file:
        return json.load(file)
def save_stats(stats):

    with open(DB_FILE, "w") as file:
        json.dump(stats, file, indent=4)

stats=load_stats()
#USER INTERFACE

import tkinter as tk

# COLORS
BG_MAIN = "#2b1d16"       # dark wood
BG_PANEL = "#4a2c1d"      # brown
BTN_WOOD = "#8b5a2b"      # wood button
BTN_HOVER = "#a06a3b"
TEXT_LIGHT = "#f5e6cc"    # parchment
GRID_COLOR = "#c89b6d"
ACCENT = "#d9b382"
# ROOT , Title
root = tk.Tk()
root.title("Nine Tiles")
root.geometry("520x620")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

#page switch
def show_frame(frame):
    frame.tkraise()

# Hover glow
def on_enter(e):
    e.widget['background'] = BTN_HOVER


def on_leave(e):
    e.widget['background'] = BTN_WOOD

#Button aesthetics
def style_button(btn):
    btn.configure(
        bg=BTN_WOOD,
        fg=TEXT_LIGHT,
        activebackground=BTN_HOVER,
        activeforeground="black",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Times New Roman", 13, "bold")
    )

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

#PAGES
menu_page = tk.Frame(root, bg=BG_MAIN)
easy_page = tk.Frame(root, bg=BG_MAIN)
medium_page = tk.Frame(root, bg=BG_MAIN)
hard_page = tk.Frame(root, bg=BG_MAIN)

for frame in (menu_page, easy_page, medium_page, hard_page):
    frame.grid(row=0, column=0, sticky="nsew")


# TITLE
menu_title = tk.Label(
    menu_page,
    text="◈ NINE TILES ◈",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=("Times New Roman", 24, "bold")
)
menu_title.pack(pady=40)

subtitle = tk.Label(
    menu_page,
    text="～ Good Luck, Wanderer ～",
    bg=BG_MAIN,
    fg=ACCENT,
    font=("Times New Roman", 14, "italic")
)
subtitle.pack(pady=5)
# MENU BUTTON
btn_easy = tk.Button(
    menu_page,
    text="Easy Mode",
    width=20,
    height=2,
    command=lambda: show_frame(easy_page)
)
style_button(btn_easy)
btn_easy.pack(pady=15)

btn_medium = tk.Button(
    menu_page,
    text="Medium Mode",
    width=20,
    height=2,
    command=lambda: show_frame(medium_page)
)
style_button(btn_medium)
btn_medium.pack(pady=15)

btn_hard = tk.Button(
    menu_page,
    text="Hard Mode (Minimax)",
    width=20,
    height=2,
    command=lambda: show_frame(hard_page)
)
style_button(btn_hard)
btn_hard.pack(pady=15)

exit_btn = tk.Button(
    menu_page,
    text="Exit",
    width=14,
    height=2,
    command=root.destroy
)
style_button(exit_btn)
exit_btn.pack(pady=35)

# GRID
def create_game_page(page, title, mode_function):

    title_label = tk.Label(
        page,
        text=title,
        bg=BG_MAIN,
        fg=TEXT_LIGHT,
        font=("Times New Roman", 20, "bold")
    )
    title_label.pack(pady=20)

    board_frame = tk.Frame(
        page,
        bg=GRID_COLOR,
        padx=10,
        pady=10
    )
    board_frame.pack(pady=20)

    buttons = []

    for row in range(3):
        button_row = []

        for col in range(3):

            btn = tk.Button(
                board_frame,
                text="",
                width=5,
                height=2,
                bg="#f5deb3",
                fg="#3b2414",
                relief="flat",
                bd=0,
                font=("Times New Roman", 28, "bold")
            )

            btn.config(
                command=lambda b=btn: mode_function(b, buttons)
            )

            btn.grid(
                row=row,
                column=col,
                padx=6,
                pady=6,
                ipadx=10,
                ipady=10
            )

            button_row.append(btn)

        buttons.append(button_row)

    back_btn = tk.Button(
        page,
        text="Return to Menu",
        width=18,
        height=2,
        command=lambda: (
            show_frame(menu_page),
            clear_btn(buttons)
        )
    )

    style_button(back_btn)
    back_btn.pack(pady=25)

    return buttons

#game pages
button_easy = create_game_page(
    easy_page,
    "🌿 Easy Mode",
    easy_mode
)

button_medium = create_game_page(
    medium_page,
    "⚔ Medium Mode",
    medium_mode
)

button_hard = create_game_page(
    hard_page,
    "🔥 Hard Mode - Minimax AI",
    hard_mode
)

#menu priority
show_frame(menu_page)
root.mainloop()
