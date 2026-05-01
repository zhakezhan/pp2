import psycopg2
from psycopg2 import OperationalError

DB_PARAMS = {
    "host":     "localhost",
    "database": "snake",
    "user":     "postgres",
    "password": "Urakbtu2025",
    "port":     2204,
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER   NOT NULL,
    level_reached INTEGER   NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
"""


def get_conn():
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="snake",
            user="postgres",
            password="Urakbtu2025",
            port=2204
        )
        return conn
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return None


def init_db():
    conn = get_conn()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(SCHEMA)
    conn.commit()
    cur.close()
    conn.close()


def get_or_create_player(username):
    conn = get_conn()
    if not conn:
        return None
    cur = conn.cursor()
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
    conn.commit()
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None


def save_session(player_id, score, level):
    conn = get_conn()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
        (player_id, score, level)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_personal_best(player_id):
    conn = get_conn()
    if not conn:
        return 0
    cur = conn.cursor()
    cur.execute(
        "SELECT COALESCE(MAX(score), 0) FROM game_sessions WHERE player_id = %s",
        (player_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else 0


def get_leaderboard():
    conn = get_conn()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached,
               TO_CHAR(gs.played_at, 'DD.MM.YY')
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY gs.score DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows