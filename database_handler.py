import sqlite3

class LeaderboardDB:
    def __init__(self, db_path='leaderboard.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Original leaderboard table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    total_time REAL NOT NULL,
                    total_moves INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # New table for picture memory game
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS picture_memory_game (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    completion_time REAL NOT NULL,
                    moves INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_score(self, username, total_time, total_moves):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO players (username, total_time, total_moves) VALUES (?, ?, ?)',
                (username, total_time, total_moves)
            )
            conn.commit()

    def get_top_players(self, limit=10):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT username, total_time, total_moves, timestamp
                FROM players 
                ORDER BY total_time ASC, total_moves ASC 
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def add_picture_game_score(self, username, completion_time, moves):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO picture_memory_game (username, completion_time, moves) VALUES (?, ?, ?)',
                (username, completion_time, moves)
            )
            conn.commit()

    def get_top_picture_players(self, limit=10):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT username, completion_time, moves, timestamp
                FROM picture_memory_game 
                ORDER BY completion_time ASC, moves ASC 
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()
