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

# Pure win-check on a 2D text board (no UI side effects)
# Checks all 8 lines: 3 rows, 3 columns, 2 diagonals
# Returns 'X', 'O', 'tie', or None (game still ongoing)
def check_board(board_text):
    """Pure win-check on a 2D text board. Returns 'X', 'O', 'tie', or None."""
    lines = [
        # rows
        [board_text[0][0],board_text[0][1],board_text[0][2]],
        [board_text[1][0],board_text[1][1],board_text[1][2]],
        [board_text[2][0],board_text[2][1],board_text[2][2]],
        # columns
        [board_text[0][0],board_text[1][0],board_text[2][0]],
        [board_text[0][1],board_text[1][1],board_text[2][1]],
        [board_text[0][2],board_text[1][2],board_text[2][2]],
        # diagonals
        [board_text[0][0],board_text[1][1],board_text[2][2]],
        [board_text[0][2],board_text[1][1],board_text[2][0]],
    ]
    for line in lines:
        if line == ["X","X","X"]: return "X"
        if line == ["O","O","O"]: return "O"
    if all(board_text[r][c] != "" for r in range(3) for c in range(3)): return "tie"  # board full, no winner
    return None

# Converts button grid to text, calls check_board, then shows the game-over dialog
# Returns 'X', 'O', 'tie' when game ends returns 0 if still in progress
def check_winner(board):

    global stats

    board_text = [[board[r][c].cget("text") for c in range(3)] for r in range(3)]

    status = check_board(board_text)

    if status == "X":

        stats["player_wins"] += 1
        stats["games_played"] += 1

        save_stats(stats)

        messagebox.showinfo(
            "Victory",
            "🎉 You Won!"
        )

        clear_btn(board)

        return "X"

    elif status == "O":

        stats["computer_wins"] += 1
        stats["games_played"] += 1

        save_stats(stats)

        messagebox.showinfo(
            "Defeat",
            "😔 Computer Won"
        )

        clear_btn(board)

        return "O"

    elif status == "tie":

        stats["draws"] += 1
        stats["games_played"] += 1

        save_stats(stats)

        messagebox.showinfo(
            "Draw",
            "😐 It's a Tie"
        )

        clear_btn(board)

        return "tie"

    return 0# Game isnt over  

# Medium AI decision logic: evaluates the board and picks the best cell for O
# Priority order: 1) win immediately  2) block X  3) positional strategy
def check_medium(cnt, board):
    board=[[board[r][c] for c in range (3)]for r in range (3)]
    empty_buttons = [b for row in board for b in row if b.cget("text") == ""]

    # Build all 8 winning lines as (text_values, button_refs) pairs
    lines = [
        # rows
        ([board[0][0].cget("text"), board[0][1].cget("text"), board[0][2].cget("text")], [board[0][0], board[0][1], board[0][2]]),
        ([board[1][0].cget("text"), board[1][1].cget("text"), board[1][2].cget("text")], [board[1][0], board[1][1], board[1][2]]),
        ([board[2][0].cget("text"), board[2][1].cget("text"), board[2][2].cget("text")], [board[2][0], board[2][1], board[2][2]]),
        # columns
        ([board[0][0].cget("text"), board[1][0].cget("text"), board[2][0].cget("text")], [board[0][0], board[1][0], board[2][0]]),
        ([board[0][1].cget("text"), board[1][1].cget("text"), board[2][1].cget("text")], [board[0][1], board[1][1], board[2][1]]),
        ([board[0][2].cget("text"), board[1][2].cget("text"), board[2][2].cget("text")], [board[0][2], board[1][2], board[2][2]]),
        # diagonals
        ([board[0][0].cget("text"), board[1][1].cget("text"), board[2][2].cget("text")], [board[0][0], board[1][1], board[2][2]]),
        ([board[0][2].cget("text"), board[1][1].cget("text"), board[2][0].cget("text")], [board[0][2], board[1][1], board[2][0]]),
    ]

    def fill_line(player):
        """If any line has 2 of `player` and 1 empty, place O in the empty cell. Returns True if placed."""
        for text_line, btn_line in lines:
            if text_line.count(player) == 2 and text_line.count("") == 1:
                btn_line[text_line.index("")].config(text="O", state=tk.DISABLED)
                return True
        return False

    # Priority 1: complete O's two-in-a-row to win
    if fill_line("O"):
        pass
    # Priority 2: block X's two-in-a-row
    elif fill_line("✕ "):
        pass
    #Other winning conditions — positional heuristics when no immediate threat exists
    elif cnt!=8:
        #if user starts from corner and plays next on side middle
        if board[1][1].cget("text")=="O" and (board[0][1].cget("text")=="" or board[1][0].cget("text")=="" or board[1][2].cget("text")=="" or board[2][1].cget("text")==""):
            if ((board[2][0].cget("text")=="✕ " and board[0][1].cget("text")=="✕") or (board[0][0].cget("text")=="X" and board[2][1].cget("text")=="✕")) and (board[1][2].cget("text")==""):
                board[1][2].config(text="O", state=tk.DISABLED)
            elif ((board[2][2].cget("text")=="✕ " and board[0][1].cget("text")=="✕") or (board[0][2].cget("text")=="X" and board[2][1].cget("text")=="✕")) and (board[1][0].cget("text")==""):
                board[1][0].config(text="O", state=tk.DISABLED)
            elif board[1][1].cget("text")=="O" and (board[0][0].cget("text")=="" or board[0][2].cget("text")=="" or board[2][0].cget("text")=="" or board[2][2].cget("text")==""):
                if ((board[2][1].cget("text")=="✕ " and board[1][2].cget("text")=="✕ ")) and (board[2][2].cget("text")==""):
                    board[2][2].config(text="O", state=tk.DISABLED)
                elif ((board[1][0].cget("text")=="✕ " and board[2][1].cget("text")=="✕ "))and (board[2][0].cget("text")==""):
                    board[2][0].config(text="O", state=tk.DISABLED)
                elif ((board[0][1].cget("text")=="✕ " and board[1][0].cget("text")=="✕ ")) and (board[0][0].cget("text")==""):
                    board[0][0].config(text="O", state=tk.DISABLED)
                elif ((board[0][1].cget("text")=="✕ " and board[1][2].cget("text")=="✕ ")) and (board[0][2].cget("text")==""):
                    board[0][2].config(text="O", state=tk.DISABLED)
                elif ((board[1][2].cget("text")=="✕ " and (board[0][0].cget("text")=="✕ " or board[2][0].cget("text")=="✕"))) and (board[2][1].cget("text")==""):
                    board[2][1].config(text="O", state=tk.DISABLED)
                elif ((board[2][1].cget("text")=="✕ " and (board[0][0].cget("text")=="✕ " or board[0][2].cget("text")=="✕"))) and (board[1][0].cget("text")==""):
                    board[1][0].config(text="O", state=tk.DISABLED)
                elif ((board[1][0].cget("text")=="✕ " and (board[0][2].cget("text")=="✕ " or board[2][2].cget("text")=="✕"))) and (board[2][1].cget("text")==""):
                    board[2][1].config(text="O", state=tk.DISABLED)
                elif ((board[0][1].cget("text")=="✕ " and (board[2][0].cget("text")=="✕ " or board[2][2].cget("text")=="✕"))) and (board[1][0].cget("text")==""):
                    board[1][0].config(text="O", state=tk.DISABLED)
                else:
                    # X on opposite corners → play an edge to avoid fork
                    if ((board[2][0].cget("text")=="X" and board[0][2].cget("text")=="X") or (board[0][0].cget("text")=="X" and board[2][2].cget("text")=="X")):
                        blank_list1=[]
                        if board[0][1].cget("text")=="":
                            blank_list1.append(board[0][1])
                        if board[1][0].cget("text")=="":
                            blank_list1.append(board[1][0])
                        if board[1][2].cget("text")=="":
                            blank_list1.append(board[1][2])
                        if board[2][1].cget("text")=="":
                            blank_list1.append(board[2][1])
                        ai_btn = random.choice(blank_list1)
                        ai_btn.config(text="O", state=tk.DISABLED)
                    else:
                        ai_btn = random.choice(empty_buttons)
                        ai_btn.config(text="O", state=tk.DISABLED)
            #if user plays 2 corners — respond with an edge to neutralise fork threat
            else:
                blank_list1=[]
                if board[0][1].cget("text")=="":
                    blank_list1.append(board[0][1])
                if board[1][0].cget("text")=="":
                    blank_list1.append(board[1][0])
                if board[1][2].cget("text")=="":
                    blank_list1.append(board[1][2])
                if board[2][1].cget("text")=="":
                    blank_list1.append(board[2][1])
                ai_btn = random.choice(blank_list1)
                ai_btn.config(text="O", state=tk.DISABLED)
        #if user starts from middle — O counters by taking a corner
        elif board[1][1].cget("text")=="✕ " and (board[0][0].cget("text")=="" or board[0][2].cget("text")=="" or board[2][0].cget("text")=="" or board[2][2].cget("text")==""):
            blank_list2=[]
            if board[0][0].cget("text")=="":
                blank_list2.append(board[0][0])
            if board[0][2].cget("text")=="":
                blank_list2.append(board[0][2])
            if board[2][0].cget("text")=="":
                blank_list2.append(board[2][0])
            if board[2][2].cget("text")=="":
                blank_list2.append(board[2][2])
            ai_btn = random.choice(blank_list2)
            ai_btn.config(text="O", state=tk.DISABLED)
        else:
            # no pattern matched — fall back to a random empty cell
            ai_btn = random.choice(empty_buttons)
            ai_btn.config(text="O", state=tk.DISABLED)

# Tries every empty cell, scores it with minimax, returns the best (row, col) for O
def best_move(board):
    """Return (row, col) of the best move for O using minimax."""
    best_score, best_pos = -100, None
    for r in range(3):
        for c in range(3):
            if board[r][c]=="":
                board[r][c]="O"           # try placing O
                score = minimax(board, False)  # score the resulting board (X moves next)
                board[r][c]=""            # undo the move
                if score > best_score:
                    best_score, best_pos = score, (r, c)
    return best_pos

# Recursive minimax: O maximises score, X minimises it
# Scores: O wins → +10, X wins → -10, tie → 0
def minimax(board, is_maximizing):
    """Minimax: O is maximiser (+10), ✕ is minimiser (-10), tie is 0."""
    result = check_board(board)
    if result=="O":   return 10   # O wins
    if result=="✕ ":   return -10  # X wins
    if result=="tie": return 0    # draw
    if is_maximizing:
        # O's turn — pick the move with the highest score
        best = -100
        for r in range(3):
            for c in range(3):
                if board[r][c]=="":
                    board[r][c]="O"
                    best = max(best, minimax(board, False))
                    board[r][c]=""  # undo
        return best
    else:
        # X's turn — pick the move with the lowest score (worst for O)
        best = 100
        for r in range(3):
            for c in range(3):
                if board[r][c]=="":
                    board[r][c]="✕ "
                    best = min(best, minimax(board, True))
                    board[r][c]=""  # undo
        return best
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
