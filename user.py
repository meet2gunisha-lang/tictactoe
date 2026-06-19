import sqlite3

# Shared current user state — set via set_current_user() after login
current_user = None

def set_current_user(username):
    global current_user
    current_user = username

def create_database():

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,
        medium_wins INTEGER DEFAULT 0,
        medium_losses INTEGER DEFAULT 0,
        games_played INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

create_database()


#REGISTERING AND PLAYER PROFILESSS

def register_user(username,password):

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username,password)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()
       

#login stuff
def login_user(username,password):

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )

    user = cursor.fetchone()

    conn.close()

    return user

#winss
def add_medium_win():

    if not current_user:
        return

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET medium_wins = medium_wins + 1,
        games_played = games_played + 1
    WHERE username = ?
    """,(current_user,))

    conn.commit()
    conn.close()

#losss
def add_medium_loss():

    if not current_user:
        return

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET medium_losses = medium_losses + 1,
        games_played = games_played + 1
    WHERE username = ?
    """,(current_user,))

    conn.commit()
    conn.close()

#leaderboard
def get_top_players():

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, medium_wins
    FROM users
    ORDER BY medium_wins DESC
    LIMIT 3
    """)

    leaders = cursor.fetchall()

    conn.close()

    return leaders