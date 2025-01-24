import sqlite3
import os

class LeaderboardDB:
    def __init__(self, db_path='leaderboard.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database with players table if not exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_score(self, username, score):
        """Add a new score to the leaderboard."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO players (username, score) VALUES (?, ?)', 
                           (username, score))
            conn.commit()

    def get_top_players(self, limit=10):
        """Retrieve top players sorted by score."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT username, score, timestamp 
                FROM players 
                ORDER BY score DESC 
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()