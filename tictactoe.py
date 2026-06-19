import tkinter as tk
from board_utils import easy_mode, medium_mode, hard_mode, clear_btn
from tkinter import messagebox, ttk
from user import *
import user as user_module


# COLORS
BG_MAIN = "#2b1d16"       
BG_PANEL = "#4a2c1d"      
BTN_WOOD = "#8b5a2b"     
BTN_HOVER = "#a06a3b"
TEXT_LIGHT = "#f5e6cc"    
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
    font=("Times New Roman", 18, "italic")
).pack(pady=5)

# USERNAME LABEL

tk.Label(
    login_page,
    text="Username",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=("Times New Roman", 14)
).pack()

username_entry = tk.Entry(login_page, width=25, font=("Times New Roman", 14))
username_entry.pack(pady=10)

# PASSWORD LABEL

tk.Label(
    login_page,
    text="Password",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=("Times New Roman", 14)
).pack()

password_entry = tk.Entry(login_page, width=25, show="*",  font=("Times New Roman", 14))
password_entry.pack(pady=10)

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
        subtitle.config(text=f"～ Good Luck, {username} ～")
        username_entry.delete(0,tk.END)
        password_entry.delete(0,tk.END)
        show_frame(menu_page)

    else:

        messagebox.showerror(
            "Error",
            "Invalid Username or Password"
        )

login_btn = tk.Button(
    login_page,
    text="Login",
    width=14,
    height=1,
    command=login_clicked
)
style_button(login_btn)
login_btn.pack(pady=10)

new_acnt_btn = tk.Button(
    login_page,
    text="Create New Account",
    width=18,
    height=1,
    command=lambda: (
        show_frame(register_page),
        username_entry.delete(0,tk.END),
        password_entry.delete(0,tk.END)
        )
)
style_button(new_acnt_btn)
new_acnt_btn.pack(pady=10)

exit_btn = tk.Button(
    login_page,
    text="Exit",
    width=14,
    height=1,
    command=root.destroy
)
style_button(exit_btn)
exit_btn.pack(pady=10)


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
    font=("Times New Roman", 18, "italic")
).pack(pady=5)

# USERNAME LABEL

tk.Label(
    register_page,
    text="Username",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=("Times New Roman", 14)
).pack()


# Register username box
new_user_entry = tk.Entry(register_page, width=25, font=("Times New Roman", 14))
new_user_entry.pack(pady=10)

# PASSWORD LABEL

tk.Label(
    register_page,
    text="Password",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=("Times New Roman", 14)
).pack()


# Register password box
new_pass_entry = tk.Entry(register_page, width=25, show="*", font=("Times New Roman", 14))
new_pass_entry.pack(pady=10)

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

create_acnt_btn = tk.Button(
    register_page,
    text="Create Account",
    width=14,
    height=1,
    command=register_clicked
)
style_button(create_acnt_btn)
create_acnt_btn.pack(pady=10)

back_login_btn = tk.Button(
    register_page,
    text="Back to Login",
    width=14,
    height=1,
    command=lambda: show_frame(login_page)
)
style_button(back_login_btn)
back_login_btn.pack(pady=10)

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
    text="Logout",
    width=14,
    height=2,
    command=lambda: show_frame(login_page)
)
style_button(exit_btn)
exit_btn.pack(pady=15)

tk.Label(
    leaderboard_page,
    text=" LEADERBOARD ",
    bg=BG_MAIN,
    fg=TEXT_LIGHT,
    font=("Times New Roman", 20, "bold")
).pack(pady=10)

lb_style = ttk.Style()
lb_style.theme_use("default")
lb_style.configure("LB.Treeview",
    background=BG_PANEL,
    foreground=TEXT_LIGHT,
    fieldbackground=BG_PANEL,
    rowheight=25,
    font=("Times New Roman", 12)
)
lb_style.configure("LB.Treeview.Heading",
    background=BTN_WOOD,
    foreground=TEXT_LIGHT,
    font=("Times New Roman", 12, "bold")
)

def make_mode_table(parent, label_text):
    tk.Label(
        parent,
        text=label_text,
        bg=BG_MAIN,
        fg=ACCENT,
        font=("Times New Roman", 12, "bold italic")
    ).pack(pady=(10, 2))
    table = ttk.Treeview(
        parent,
        style="LB.Treeview",
        columns=("rank", "name", "wins", "ties"),
        show="headings",
        height=4
    )
    table.heading("rank", text="#")
    table.heading("name", text="Player")
    table.heading("wins", text="Wins")
    table.heading("ties", text="Ties")
    table.column("rank", width=40,  anchor="center")
    table.column("name", width=160, anchor="center")
    table.column("wins", width=70,  anchor="center")
    table.column("ties", width=70,  anchor="center")
    table.pack(pady=(0, 8))
    return table

lb_table_easy   = make_mode_table(leaderboard_page, "🌿 Easy Mode")
lb_table_medium = make_mode_table(leaderboard_page, "⚔ Medium Mode")
lb_table_hard   = make_mode_table(leaderboard_page, "🔥 Hard Mode")

def fill_table(table, mode):
    for row in table.get_children():
        table.delete(row)

    top3 = get_top_players_by_mode(mode, limit=3)
    top3_names = {name for name, _, _ in top3}

    rank, prev_wins, prev_ties = 1, None, None
    i = 0
    for  (name, wins, ties) in top3:
        if (wins != prev_wins or  ties != prev_ties):
            rank = i + 1
        prev_wins = wins
        prev_ties = ties
        table.insert("", tk.END, values=(rank, name, wins, ties))
        i = i+1

    me = user_module.current_user
    if me and me not in top3_names:
        stats = get_user_stats_by_mode(mode, me)
        if stats:
            my_wins, my_ties = stats

            if (my_wins == prev_wins and my_ties == prev_ties):
                my_rank = rank
            else:
                my_rank = get_count_above_score(mode, my_wins, my_ties) + 1

            table.insert("", tk.END, values=(my_rank, f"{me} ★", my_wins, my_ties))

def refresh_leaderboard():
    fill_table(lb_table_easy,   "easy")
    fill_table(lb_table_medium, "medium")
    fill_table(lb_table_hard,   "hard")


back_btn = tk.Button(
        leaderboard_page,
        text="Return to Menu",
        width=18,
        height=2,
        command=lambda:show_frame(menu_page)
    )

style_button(back_btn)
back_btn.pack(pady=10)

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
btn_leaderboard.pack(pady=10)

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

show_frame(login_page)
root.mainloop()