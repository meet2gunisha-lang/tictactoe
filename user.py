import sqlite3
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
        
        easy_wins INTEGER DEFAULT 0,
        easy_losses INTEGER DEFAULT 0,
        easy_ties INTEGER DEFAULT 0,
        
        medium_losses INTEGER DEFAULT 0,
        medium_wins INTEGER DEFAULT 0,
        medium_ties INTEGER DEFAULT 0,
        
        hard_wins INTEGER DEFAULT 0,
        hard_losses INTEGER DEFAULT 0,
        hard_ties INTEGER DEFAULT 0,

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
def add_easy_win():


    if not current_user:
        return

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET easy_wins = easy_wins + 1,
        games_played = games_played + 1
    WHERE username = ?
    """,(current_user,))

    conn.commit()
    conn.close()

#losss
def add_easy_loss():

    if not current_user:
        return

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET easy_losses = easy_losses + 1,
        games_played = games_played + 1
    WHERE username = ?
    """,(current_user,))

    conn.commit()
    conn.close()


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



#winss
def add_hard_win():


    if not current_user:
        return

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET hard_wins = hard_wins + 1,
        games_played = games_played + 1
    WHERE username = ?
    """,(current_user,))

    conn.commit()
    conn.close()

#losss
def add_hard_loss():

    if not current_user:
        return

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET hard_losses = hard_losses + 1,
        games_played = games_played + 1
    WHERE username = ?
    """,(current_user,))

    conn.commit()
    conn.close()



#winss
def add_easy_tie():


    if not current_user:
        return

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET easy_ties = easy_ties + 1,
        games_played = games_played + 1
    WHERE username = ?
    """,(current_user,))

    conn.commit()
    conn.close()

#losss
def add_medium_ties():

    if not current_user:
        return

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET medium_ties = medium_ties + 1,
        games_played = games_played + 1
    WHERE username = ?
    """,(current_user,))

    conn.commit()
    conn.close()




#winss
def add_hard_ties():


    if not current_user:
        return

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET hard_ties = hard_ties + 1,
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
    SELECT username, medium_wins + easy_wins + hard_wins,
        medium_losses + easy_losses + hard_losses,
        medium_ties + easy_ties + hard_ties,
        games_played
    FROM users
    ORDER BY medium_wins + easy_wins + hard_wins DESC
    LIMIT 3
    """)

    leaders = cursor.fetchall()

    conn.close()

    return leaders
