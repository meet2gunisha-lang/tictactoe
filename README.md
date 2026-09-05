# tictactoe

git add .

git commit -m "change"
git push 

py -m pip install mysql-connector-python

connect root@localhost ;

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';

## Database backend: SQLite vs MySQL

Login, registration, and per-mode win/loss/tie stats are handled by a
database module that `tictactoe.py` and `board_utils.py` import. Two
interchangeable implementations exist, exposing the identical function
set (`set_current_user`, `register_user`, `login_user`, `add_status`,
`get_top_players_by_mode`, `get_user_stats_by_mode`,
`get_count_above_score`), so switching between them is a one-line change.

### `user.py` — SQLite (default, zero setup)

- Stores everything in a local file `nine_tiles.db` in the project folder.
- No server, install, or credentials required — the file/table are
  created automatically the first time the app runs.
- Best choice when MySQL isn't installed, or for quick local testing.

### `mysql_user.py` — MySQL (requires a running server)

- Connects to a real MySQL server using the `DB_CONFIG` dict at the top
  of the file (`host`, `user`, `password`, `database`). Update these to
  match your local MySQL setup before running.
- The `nine_tiles` database and `users` table are created automatically
  on first run if they don't already exist.
- Requires `mysql-connector-python` (see install command above) and a
  MySQL server actually running and reachable at `DB_CONFIG["host"]`.

### How to switch

Both `tictactoe.py` and `board_utils.py` import the active backend the
same way:

```python
from user import *          # SQLite (default)
import user as user_module
```

To switch to MySQL, change both imports in **both** files to:

```python
from mysql_user import *          # MySQL
import mysql_user as user_module
```

(and back again to switch to SQLite). Make sure to update both files
consistently — mixing backends between `tictactoe.py` and
`board_utils.py` will cause `current_user` state to be tracked in two
separate places and break login/stat updates.
