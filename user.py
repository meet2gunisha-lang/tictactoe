import sqlite3

# Username of the currently logged-in player, set by set_current_user()
# after a successful login. Used by add_status() to know whose stats
# to update, and by the UI to show "logged in as ..." / leaderboard rank.
current_user = None

def set_current_user(username):
    """Store the logged-in player's username for later stat updates."""
    global current_user
    current_user = username

def create_database():
    """Ensure the local 'nine_tiles.db' SQLite file and 'users' table
    exist. Called once at import time (see create_database() call below)
    so the app can run with zero setup - no server, no credentials.
    """
    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    # One row per user, with separate win/loss/tie counters for each
    # difficulty mode (easy/medium/hard) plus a running total of games played.
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

# Run once on import so the schema is guaranteed to exist before any
# other function in this module (or in tictactoe.py / board_utils.py) runs.
create_database()


def register_user(username,password):
    """Create a new user account.
    Returns True on success, False if the username is already taken
    (caught via the PRIMARY KEY uniqueness constraint on `username`).
    """
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
        # Raised when the username already exists (duplicate primary key)
        return False

    finally:
        # Always release the connection, whether the insert succeeded or not
        conn.close()


def login_user(username,password):
    """Validate credentials against the users table.
    Returns the matching row (truthy) if the username/password pair is
    correct, or None (falsy) if no match is found.
    """
    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def add_status(mode, status):
    """Increment a single stat column for the current user.

    mode:   'easy' | 'medium' | 'hard'
    status: 'wins' | 'losses' | 'ties'

    Builds the column name dynamically (e.g. "easy_wins") and bumps both
    that column and the overall games_played counter by 1. No-op if no
    user is currently logged in.
    """

    if not current_user:
        return

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()

    cursor.execute(f"""
    UPDATE users
    SET {mode}_{status} = {mode}_{status} + 1,
        games_played = games_played + 1
    WHERE username = ?
    """,(current_user,))

    conn.commit()
    conn.close()

def get_top_players_by_mode(mode, limit=3):
    """Return the top `limit` players for a given mode.

    Ranked by wins (descending), with ties as a tiebreaker.
    Returns a list of (username, wins, ties) tuples - used to populate
    the leaderboard table for that mode.
    """

    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT username, {mode}_wins AS wins, {mode}_ties AS ties
    FROM users
    ORDER BY {mode}_wins DESC, {mode}_ties DESC
    LIMIT ?
    """, (limit,))
    leaders = cursor.fetchall()
    conn.close()
    return leaders

def get_user_stats_by_mode(mode, username):
    """Return (wins, ties) for a specific user in a specific mode.
    Used to display the current user's own stats on the leaderboard,
    even if they didn't make the top 3.
    """
    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT {mode}_wins, {mode}_ties FROM users WHERE username = ?
    """, (username,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_count_above_score(mode, wins, ties):
    """Count how many players outrank the given (wins, ties) score.

    A player outranks another if they have strictly more wins, OR the
    same wins but strictly more ties. Adding 1 to this count gives the
    1-based rank of a player with this exact (wins, ties) combination -
    used to compute the current user's leaderboard position.
    """
    conn = sqlite3.connect("nine_tiles.db")
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT COUNT(*) FROM users
    WHERE {mode}_wins > ? or ( {mode}_wins = ? and {mode}_ties > ? )
    """, (wins, wins, ties))
    count = cursor.fetchone()[0]
    conn.close()
    return count
