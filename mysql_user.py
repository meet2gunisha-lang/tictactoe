import mysql.connector

# ── DB connection config ──────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",       # change to your MySQL username
    "password": "",           # change to your MySQL password
    "database": "nine_tiles"
}

current_user = None

def set_current_user(username):
    global current_user
    current_user = username

def _connect():
    return mysql.connector.connect(**DB_CONFIG)

def create_database():
    cfg = DB_CONFIG.copy()
    db_name = cfg.pop("database")
    conn = mysql.connector.connect(**cfg)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
    cursor.execute(f"USE `{db_name}`")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT,

        easy_wins    INTEGER DEFAULT 0,
        easy_losses  INTEGER DEFAULT 0,
        easy_ties    INTEGER DEFAULT 0,

        medium_losses INTEGER DEFAULT 0,
        medium_wins   INTEGER DEFAULT 0,
        medium_ties   INTEGER DEFAULT 0,

        hard_wins    INTEGER DEFAULT 0,
        hard_losses  INTEGER DEFAULT 0,
        hard_ties    INTEGER DEFAULT 0,

        games_played INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

create_database()


#REGISTERING AND PLAYER PROFILESSS

def register_user(username, password):

    conn = _connect()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        return True

    except mysql.connector.IntegrityError:
        return False

    finally:
        cursor.close()
        conn.close()


def login_user(username, password):

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return user


def add_status(mode, status):

    if not current_user:
        return

    conn = _connect()
    cursor = conn.cursor()

    cursor.execute(f"""
    UPDATE users
    SET {mode}_{status} = {mode}_{status} + 1,
        games_played = games_played + 1
    WHERE username = %s
    """, (current_user,))

    conn.commit()
    cursor.close()
    conn.close()

def get_top_players_by_mode(mode, limit=3):

    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT username, {mode}_wins AS wins, {mode}_ties AS ties
    FROM users
    ORDER BY {mode}_wins DESC, {mode}_ties DESC
    LIMIT %s
    """, (limit,))
    leaders = cursor.fetchall()
    cursor.close()
    conn.close()
    return leaders

def get_user_stats_by_mode(mode, username):

    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT {mode}_wins, {mode}_ties FROM users WHERE username = %s
    """, (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def get_count_above_score(mode, wins, ties):

    conn = _connect()
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT COUNT(*) FROM users
    WHERE {mode}_wins > %s OR ( {mode}_wins = %s AND {mode}_ties > %s )
    """, (wins, wins, ties))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count
