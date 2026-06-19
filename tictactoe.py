import tkinter as tk
from board_utils import easy_mode, medium_mode, hard_mode, clear_btn
from tkinter import messagebox
from user import register_user, login_user, get_top_players, set_current_user


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
root.geometry("520x640")
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
login_page = tk.Frame(root, bg=BG_MAIN)
register_page = tk.Frame(root, bg=BG_MAIN)

menu_page = tk.Frame(root, bg=BG_MAIN)
easy_page = tk.Frame(root, bg=BG_MAIN)
medium_page = tk.Frame(root, bg=BG_MAIN)
hard_page = tk.Frame(root, bg=BG_MAIN)
leaderboard_page=tk.Frame(root,bg=BG_MAIN)

for frame in (login_page,register_page,menu_page, easy_page, medium_page, hard_page,leaderboard_page):
    frame.grid(row=0, column=0, sticky="nsew")

#LOGIN PAGESS
tk.Label(
    login_page,
    text="◈ NINE TILES ◈",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=("Times New Roman", 24, "bold")
).pack(pady=30)

tk.Label(
    login_page,
    text="Login to Continue",
    bg=BG_MAIN,
    fg=ACCENT,
    font=("Times New Roman", 12, "italic")
).pack(pady=5)

# USERNAME LABEL

tk.Label(
    login_page,
    text="Username",
    bg=BG_MAIN,
    fg=TEXT_LIGHT
).pack()

username_entry = tk.Entry(login_page, width=25)
username_entry.pack(pady=5)

# PASSWORD LABEL

tk.Label(
    login_page,
    text="Password",
    bg=BG_MAIN,
    fg=TEXT_LIGHT
).pack()

password_entry = tk.Entry(login_page, width=25, show="*")
password_entry.pack(pady=5)

def login_clicked():

    global current_user

    username = username_entry.get()
    password = password_entry.get()

    if login_user(username, password):

        set_current_user(username)
        
        messagebox.showinfo(
            "Success",
            f"Welcome {username}"
        )

        show_frame(menu_page)

    else:

        messagebox.showerror(
            "Error",
            "Invalid Username or Password"
        )

tk.Button(
    login_page,
    text="Login",
    command=login_clicked
).pack(pady=10)

tk.Button(
    login_page,
    text="Create New Account",
    command=lambda: show_frame(register_page)
).pack(pady=5)

#registerrr

#LOGIN PAGESS
tk.Label(
    register_page,
    text="◈ NINE TILES ◈",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=("Times New Roman", 24, "bold")
).pack(pady=30)

tk.Label(
    register_page,
    text="Login to Continue",
    bg=BG_MAIN,
    fg=ACCENT,
    font=("Times New Roman", 12, "italic")
).pack(pady=5)

# USERNAME LABEL

tk.Label(
    register_page,
    text="Username",
    bg=BG_MAIN,
    fg=TEXT_LIGHT
).pack()


# Register username box
new_user_entry = tk.Entry(register_page, width=25)
new_user_entry.pack(pady=5)

# PASSWORD LABEL

tk.Label(
    register_page,
    text="Password",
    bg=BG_MAIN,
    fg=TEXT_LIGHT
).pack()


# Register password box
new_pass_entry = tk.Entry(register_page, width=25, show="*")
new_pass_entry.pack(pady=5)

def register_clicked():
    
    username = new_user_entry.get().strip()
    password = new_pass_entry.get().strip()

    if not username or not password:
        messagebox.showerror(
            "Error",
            "Username and Password are required"
        )
        

    elif register_user(username, password):

        messagebox.showinfo(
            "Success",
            "Account Created"
        )

        show_frame(login_page)

    else:

        messagebox.showerror(
            "Error",
            "Username Already Exists"
        )

tk.Button(
    register_page,
    text="Create Account",
    command=register_clicked
).pack(pady=10)

tk.Button(
    register_page,
    text="Back to Login",
    command=lambda: show_frame(login_page)
).pack(pady=10)

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

#leaderboard page stuff
# LEADERBOARD PAGE

tk.Label(
    leaderboard_page,
    text=" LEADERBOARD ",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=("Times New Roman", 22, "bold")
).pack(pady=20)

leaderboard_text = tk.Text(
    leaderboard_page,
    height=20,
    width=40,
    font=("Times New Roman", 14)
)

leaderboard_text.pack(pady=20)

def refresh_leaderboard():

    leaderboard_text.config(state="normal")
    leaderboard_text.delete("1.0", tk.END)

    players = get_top_players()

    rank = 1

    for name, wins, losses, ties, total in players:

        leaderboard_text.insert(
            tk.END,
            f"{rank}. {name}:  {wins} Wins, {ties} Ties\n"
        )

        rank += 1

    leaderboard_text.config(state="disabled")

tk.Button(
    leaderboard_page,
    text="Back",
    command=lambda: show_frame(menu_page)
).pack(pady=10)

btn_leaderboard = tk.Button(
    menu_page,
    text="Leaderboard",
    width=20,
    height=2,
    command=lambda: (
        refresh_leaderboard(),
        show_frame(leaderboard_page)
    )
)

style_button(btn_leaderboard)
btn_leaderboard.pack(pady=15)

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
                padx=5,
                pady=5,
                ipadx=8,
                ipady=8
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
show_frame(login_page)
root.mainloop()