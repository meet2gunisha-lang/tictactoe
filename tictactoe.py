import tkinter as tk
import random
from tkinter import messagebox


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

tk.Button(menu_page, text="Exit", width=10, bg="purple", 
          command=root.destroy).pack(pady=20)

def Replace_x(btn):
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        # flatten + filter for empty buttons
        empty_buttons = [b for row in button_easy for b in row if b.cget("text") == ""]
        win=Winner(button_easy)
        if win==0:
            if empty_buttons:     # only if any are left
                ai_btn = random.choice(empty_buttons)
                ai_btn.config(text="O", state=tk.DISABLED)
        Winner(button_easy)

def clear_btn(buttons):
    not_empty_buttons = [b for row in buttons for b in row ]
    for i in not_empty_buttons:  
            i.config(text="",state=tk.NORMAL)


def Winner(buttons):
    board = [[buttons[r][c].cget("text") for c in range(3)] for r in range(3)]
    hori_1=[board[0][0],board[0][1],board[0][2]]
    hori_2=[board[1][0],board[1][1],board[1][2]]
    hori_3=[board[2][0],board[2][1],board[2][2]]
    ver_1=[board[0][0],board[1][0],board[2][0]]
    ver_2=[board[0][1],board[1][1],board[2][1]]
    ver_3=[board[0][2],board[1][2],board[2][2]]
    diag_1=[board[0][0],board[1][1],board[2][2]]
    diag_2=[board[0][2],board[1][1],board[2][0]]
    empty=[b for row in buttons for b in row if b.cget("text")==""]

    if hori_1==["X","X","X"] or hori_2==["X","X","X"] or hori_3==["X","X","X"]:
        messagebox.showinfo("Game Over","YOU WON 🎉")
        clear_btn(buttons)
        return 1
    elif hori_1==["O","O","O"] or hori_2==["O","O","O"] or hori_3==["O","O","O"]:
        messagebox.showinfo("Game Over","Computer Won 😔")
        clear_btn(buttons)
        return 1
    elif ver_1==["X","X","X"] or ver_2==["X","X","X"] or ver_3==["X","X","X"]:
        messagebox.showinfo("Game Over","YOU WON 🎉")
        clear_btn(buttons)
        return 1
    elif ver_1==["O","O","O"] or ver_2==["O","O","O"] or ver_3==["O","O","O"]:
        messagebox.showinfo("Game Over","Computer Won 😔")
        clear_btn(buttons)
        return 1
    elif diag_1==["X","X","X"] or diag_2==["X","X","X"]:
        messagebox.showinfo("Game Over","YOU WON 🎉")
        clear_btn(buttons)
        return 1
    elif diag_1==["O","O","O"] or diag_2==["O","O","O"]:
        messagebox.showinfo("Game Over","Computer Won 😔")
        clear_btn(buttons)
        return 1
    elif len(empty)==0:
        messagebox.showinfo("Game Over","Tie 🪢")
        clear_btn(buttons)
        return 1
    return 0

#Computer logic
def new_auto_x(btn):
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        # flatten + filter for empty buttons
        board=[[button_medium[r][c] for c in range (3)]for r in range (3)]
        empty_buttons = [b for row in button_medium for b in row if b.cget("text") == ""]
        cnt=len(empty_buttons)
        win=Winner(button_medium)
        if cnt==0:
            win=Winner(button_medium)
        elif win==0:
            check(cnt)
        if cnt==8:
            if board[1][1].cget("text")=="X" :
                ai_btn = random.choice([board[0][0], board[0][2],board[2][0], board[2][2]])
                ai_btn.config(text="O", state=tk.DISABLED)
            else:
                board[1][1].config(text="O", state=tk.DISABLED)
        Winner(button_medium)

def check(cnt):
    board=[[button_medium[r][c] for c in range (3)]for r in range (3)]
    empty_buttons = [b for row in button_medium for b in row if b.cget("text") == ""]
    hori_1=[board[0][0].cget("text"),board[0][1].cget("text"),board[0][2].cget("text")]
    hori_2=[board[1][0].cget("text"),board[1][1].cget("text"),board[1][2].cget("text")]
    hori_3=[board[2][0].cget("text"),board[2][1].cget("text"),board[2][2].cget("text")]
    ver_1=[board[0][0].cget("text"),board[1][0].cget("text"),board[2][0].cget("text")]
    ver_2=[board[0][1].cget("text"),board[1][1].cget("text"),board[2][1].cget("text")]
    ver_3=[board[0][2].cget("text"),board[1][2].cget("text"),board[2][2].cget("text")]
    diag_1=[board[0][0].cget("text"),board[1][1].cget("text"),board[2][2].cget("text")]
    diag_2=[board[0][2].cget("text"),board[1][1].cget("text"),board[2][0].cget("text")]
    # See if AI is winning
    if hori_1==["O","O",""]:
        board[0][2].config(text="O", state=tk.DISABLED)
    elif hori_1==["O","","O"]:
        board[0][1].config(text="O", state=tk.DISABLED)
    elif hori_1==["","O","O"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif hori_2==["O","O",""]:
        board[1][2].config(text="O", state=tk.DISABLED)
    elif hori_2==["O","","O"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif hori_2==["","O","O"]:
        board[1][0].config(text="O", state=tk.DISABLED)
    elif hori_3==["O","O",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif hori_3==["O","","O"]:
        board[2][1].config(text="O", state=tk.DISABLED)
    elif hori_3==["","O","O"]:
        board[2][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["O","O",""] :
        board[2][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["O","","O"]:
        board[1][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["","O","O"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif ver_2==["O","O",""]:
        board[2][1].config(text="O", state=tk.DISABLED)
    elif ver_2==["O","","O"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif ver_2==["","O","O"]:
        board[0][1].config(text="O", state=tk.DISABLED)
    elif ver_3==["O","O",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif ver_3==["O","","O"]:
        board[1][2].config(text="O", state=tk.DISABLED)
    elif ver_3==["","O","O"]:
        board[0][2].config(text="O", state=tk.DISABLED)
    elif diag_1==["O","O",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif diag_1==["O","","O"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif diag_1==["","O","O"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif diag_2==["O","O",""]:
        board[2][0].config(text="O", state=tk.DISABLED)
    elif diag_2==["O","","O"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif diag_2==["","O","O"]:
        board[0][2].config(text="O", state=tk.DISABLED)
    # Check to block user
    elif hori_1==["X","X",""]:
        board[0][2].config(text="O", state=tk.DISABLED)
    elif hori_1==["X","","X"]:
        board[0][1].config(text="O", state=tk.DISABLED)
    elif hori_1==["","X","X"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif hori_2==["X","X",""]:
        board[1][2].config(text="O", state=tk.DISABLED)
    elif hori_2==["X","","X"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif hori_2==["","X","X"]:
        board[1][0].config(text="O", state=tk.DISABLED)
    elif hori_3==["X","X",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif hori_3==["X","","X"]:
        board[2][1].config(text="O", state=tk.DISABLED)
    elif hori_3==["","X","X"]:
        board[2][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["X","X",""] :
        board[2][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["X","","X"]:
        board[1][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["","X","X"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif ver_2==["X","X",""]:
        board[2][1].config(text="O", state=tk.DISABLED)
    elif ver_2==["X","","X"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif ver_2==["","X","X"]:
        board[0][1].config(text="O", state=tk.DISABLED)
    elif ver_3==["X","X",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif ver_3==["X","","X"]:
        board[1][2].config(text="O", state=tk.DISABLED)
    elif ver_3==["","X","X"]:
        board[0][2].config(text="O", state=tk.DISABLED)
    elif diag_1==["X","X",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif diag_1==["X","","X"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif diag_1==["","X","X"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif diag_2==["X","X",""]:
        board[2][0].config(text="O", state=tk.DISABLED)
    elif diag_2==["X","","X"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif diag_2==["","X","X"]:
        board[0][2].config(text="O", state=tk.DISABLED)
    #Other winning conditions
    elif cnt!=8:
        #if user starts from corner and plays next on side middle
        if board[1][1].cget("text")=="O" and (board[0][1].cget("text")=="" or board[1][0].cget("text")=="" or board[1][2].cget("text")=="" or board[2][1].cget("text")==""):
            if ((board[2][0].cget("text")=="X" and board[0][1].cget("text")=="X") or (board[0][0].cget("text")=="X" and board[2][1].cget("text")=="X")) and (board[1][2].cget("text")==""):
                board[1][2].config(text="O", state=tk.DISABLED)
            elif ((board[2][2].cget("text")=="X" and board[0][1].cget("text")=="X") or (board[0][2].cget("text")=="X" and board[2][1].cget("text")=="X")) and (board[1][0].cget("text")==""):
                board[1][0].config(text="O", state=tk.DISABLED)
            elif board[1][1].cget("text")=="O" and (board[0][0].cget("text")=="" or board[0][2].cget("text")=="" or board[2][0].cget("text")=="" or board[2][2].cget("text")==""):
                if ((board[2][1].cget("text")=="X" and board[1][2].cget("text")=="X")) and (board[2][2].cget("text")==""):
                    board[2][2].config(text="O", state=tk.DISABLED)
                elif ((board[1][0].cget("text")=="X" and board[2][1].cget("text")=="X"))and (board[2][0].cget("text")==""):
                    board[2][0].config(text="O", state=tk.DISABLED)
                elif ((board[0][1].cget("text")=="X" and board[1][0].cget("text")=="X")) and (board[0][0].cget("text")==""):
                    board[0][0].config(text="O", state=tk.DISABLED)
                elif ((board[0][1].cget("text")=="X" and board[1][2].cget("text")=="X")) and (board[0][2].cget("text")==""):
                    board[0][2].config(text="O", state=tk.DISABLED)
                elif ((board[1][2].cget("text")=="X" and (board[0][0].cget("text")=="X" or board[2][0].cget("text")=="X"))) and (board[2][1].cget("text")==""):
                    board[2][1].config(text="O", state=tk.DISABLED)
                elif ((board[2][1].cget("text")=="X" and (board[0][0].cget("text")=="X" or board[0][2].cget("text")=="X"))) and (board[1][0].cget("text")==""):
                    board[1][0].config(text="O", state=tk.DISABLED)
                elif ((board[1][0].cget("text")=="X" and (board[0][2].cget("text")=="X" or board[2][2].cget("text")=="X"))) and (board[2][1].cget("text")==""):
                    board[2][1].config(text="O", state=tk.DISABLED)
                elif ((board[0][1].cget("text")=="X" and (board[2][0].cget("text")=="X" or board[2][2].cget("text")=="X"))) and (board[1][0].cget("text")==""):
                    board[1][0].config(text="O", state=tk.DISABLED)
                else:
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
            #if user plays 2 corners
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
        #if user starts from middle
        elif board[1][1].cget("text")=="X" and (board[0][0].cget("text")=="" or board[0][2].cget("text")=="" or board[2][0].cget("text")=="" or board[2][2].cget("text")==""):
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
            ai_btn = random.choice(empty_buttons)
            ai_btn.config(text="O", state=tk.DISABLED)



# ── Minimax helpers ─────────────────────────────────────────────────────────
def minimax_check(board):
    """Check board state. Returns 'X', 'O', 'tie', or None (game ongoing)."""
    lines = [
        [board[0][0],board[0][1],board[0][2]],
        [board[1][0],board[1][1],board[1][2]],
        [board[2][0],board[2][1],board[2][2]],
        [board[0][0],board[1][0],board[2][0]],
        [board[0][1],board[1][1],board[2][1]],
        [board[0][2],board[1][2],board[2][2]],
        [board[0][0],board[1][1],board[2][2]],
        [board[0][2],board[1][1],board[2][0]],
    ]
    for line in lines:
        if line==["X","X","X"]: return "X"
        if line==["O","O","O"]: return "O"
    if all(board[r][c]!="" for r in range(3) for c in range(3)): return "tie"
    return None

def minimax(board, is_maximizing):
    """Minimax: O is maximiser (+10), X is minimiser (-10), tie is 0."""
    result = minimax_check(board)
    if result=="O":   return 10
    if result=="X":   return -10
    if result=="tie": return 0
    if is_maximizing:
        best = -100
        for r in range(3):
            for c in range(3):
                if board[r][c]=="":
                    board[r][c]="O"
                    best = max(best, minimax(board, False))
                    board[r][c]=""
        return best
    else:
        best = 100
        for r in range(3):
            for c in range(3):
                if board[r][c]=="":
                    board[r][c]="X"
                    best = min(best, minimax(board, True))
                    board[r][c]=""
        return best

def best_move(board):
    """Return (row, col) of the best move for O using minimax."""
    best_score, best_pos = -100, None
    for r in range(3):
        for c in range(3):
            if board[r][c]=="":
                board[r][c]="O"
                score = minimax(board, False)
                board[r][c]=""
                if score > best_score:
                    best_score, best_pos = score, (r, c)
    return best_pos

#Computer logic
def minimax_hard(btn):
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        board_text=[[button_hard[r][c].cget("text") for c in range(3)] for r in range(3)]
        empty_buttons=[b for row in button_hard for b in row if b.cget("text")==""]
        cnt=len(empty_buttons)
        win=Winner(button_hard)
        if cnt==0:
            win=Winner(button_hard)
        elif win==0:
            pos=best_move(board_text)
            if pos:
                r,c=pos
                button_hard[r][c].config(text="O",state=tk.DISABLED)
        Winner(button_hard)



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
        btn.config(command=lambda b=btn:Replace_x(b))
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
        btn.config(command=lambda b=btn:new_auto_x(b))
        btn.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(btn)
    button_medium.append(button_row)

tk.Button(medium_page, text="Back to Menu", command=lambda: (show_frame(menu_page),clear_btn(button_medium))).pack()


# --- HARD PAGE ---
tk.Label(hard_page, text="Hard Mode 🔵", bg="lightblue",
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
        btn.config(command=lambda b=btn:minimax_hard(b))
        btn.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(btn)
    button_hard.append(button_row)

tk.Button(hard_page, text="Back to Menu", command=lambda: (show_frame(menu_page),clear_btn(button_hard))).pack()

# --- Show the main menu first ---
show_frame(menu_page)
root.mainloop()
