import tkinter as tk
import random
from tkinter import messagebox

x=input("Enter name:")
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
        win=Winner(buttons)
        if win==0:
            if empty_buttons:     # only if any are left
                ai_btn = random.choice(empty_buttons)
                ai_btn.config(text="O", state=tk.DISABLED)
        Winner(buttons)

def clear_btn(buttons):
    not_empty_buttons = [b for row in buttons for b in row ]
    for i in not_empty_buttons:  
            i.config(text="",state=tk.NORMAL)

def Winner(buttons):
    board=[[buttons[r][c].cget("text") for c in range (3)]for r in range (3)]
    hori_1=[board[0][0],board[0][1],board[0][2]]
    hori_2=[board[1][0],board[1][1],board[1][2]]
    hori_3=[board[2][0],board[2][1],board[2][2]]
    ver_1=[board[0][0],board[1][0],board[2][0]]
    ver_2=[board[0][1],board[1][1],board[2][1]]
    ver_3=[board[0][2],board[1][2],board[2][2]]
    diag_1=[board[0][0],board[1][1],board[2][2]]
    diag_2=[board[0][2],board[1][1],board[2][0]]
    y=x,"Won"
    empty_buttons = [b for row in buttons for b in row if b.cget("text") == ""]
    if hori_1==["X","X","X"] or hori_2==["X","X","X"] or hori_3==["X","X","X"]:
        messagebox.showinfo("Game Over",y)
        clear_btn(buttons)
        return 1
    elif hori_1==["O","O","O"] or hori_2==["O","O","O"] or hori_3==["O","O","O"]:
        messagebox.showinfo("Game Over"," O Won")
        clear_btn(buttons)
        return 1
    elif ver_1==["X","X","X"] or ver_2==["X","X","X"] or ver_3==["X","X","X"]:
        messagebox.showinfo("Game Over",y)
        clear_btn(buttons)
        return 1
    elif ver_1==["O","O","O"] or ver_2==["O","O","O"] or ver_3==["O","O","O"]:
        messagebox.showinfo("Game Over"," O Won")
        clear_btn(buttons)
        return 1
    elif diag_1==["X","X","X"] or diag_2==["X","X","X"] :
        messagebox.showinfo("Game Over",y)
        clear_btn(buttons)
        return 1
    elif diag_1==["O","O","O"] or diag_2==["O","O","O"]:
        messagebox.showinfo("Game Over"," O Won")
        clear_btn(buttons)
        return 1
    elif len(empty_buttons)==0:
        messagebox.showinfo("Game Over","Tie")
        clear_btn(buttons)
        return 1
    else:
        return 0


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
tk.Button(easy_page, text="Back to Menu", command=lambda: (show_frame(menu_page),clear_btn(buttons))).pack(pady=10)

#Computer logic
def new_auto_x(btn):
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        # flatten + filter for empty buttons
        board=[[button[r][c] for c in range (3)]for r in range (3)]
        empty_buttons = [b for row in button for b in row if b.cget("text") == ""]
        cnt=len(empty_buttons)
        win=Winner(button)
        if cnt==0:
            win=Winner(button)
        elif win==0:
            check(cnt)
        if cnt==8:
            if board[1][1].cget("text")=="X" :
                ai_btn = random.choice([board[0][0], board[0][2],board[2][0], board[2][2]])
                ai_btn.config(text="O", state=tk.DISABLED)
            else:
                board[1][1].config(text="O", state=tk.DISABLED)
        Winner(button)


def check(cnt):
    board=[[button[r][c] for c in range (3)]for r in range (3)]
    empty_buttons = [b for row in button for b in row if b.cget("text") == ""]
    hori_1=[board[0][0].cget("text"),board[0][1].cget("text"),board[0][2].cget("text")]
    hori_2=[board[1][0].cget("text"),board[1][1].cget("text"),board[1][2].cget("text")]
    hori_3=[board[2][0].cget("text"),board[2][1].cget("text"),board[2][2].cget("text")]
    ver_1=[board[0][0].cget("text"),board[1][0].cget("text"),board[2][0].cget("text")]
    ver_2=[board[0][1].cget("text"),board[1][1].cget("text"),board[2][1].cget("text")]
    ver_3=[board[0][2].cget("text"),board[1][2].cget("text"),board[2][2].cget("text")]
    diag_1=[board[0][0].cget("text"),board[1][1].cget("text"),board[2][2].cget("text")]
    diag_2=[board[0][2].cget("text"),board[1][1].cget("text"),board[2][0].cget("text")]
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
    elif cnt!=8:
        if board[1][1].cget("text")=="O" and (board[0][1].cget("text")=="" or board[1][0].cget("text")=="" or board[1][2].cget("text")=="" or board[2][1].cget("text")==""):
            if ((board[2][0].cget("text")=="X" and board[0][1].cget("text")=="X") or (board[0][0].cget("text")=="X" and board[2][1].cget("text")=="X")) and (board[1][2].cget("text")==""):
                    board[1][2].config(text="O", state=tk.DISABLED)
            elif ((board[2][2].cget("text")=="X" and board[0][1].cget("text")=="X") or (board[0][2].cget("text")=="X" and board[2][1].cget("text")=="X")) and (board[1][0].cget("text")==""):
                    board[1][0].config(text="O", state=tk.DISABLED)
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
        btn = tk.Button(grid_frame, text="", width=5, height=2, font=("Arial", 18))
        btn.config(command=lambda b=btn:new_auto_x(b))
        btn.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(btn)
    button.append(button_row)


tk.Button(hard_page, text="Back to Menu", command=lambda: (show_frame(menu_page),clear_btn(button))).pack()

# --- Show the main menu first ---
show_frame(menu_page)

# --- Start the app ---
root.mainloop()
