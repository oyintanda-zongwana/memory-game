# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from database_handler import LeaderboardDB

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize database only if needed
try:
    leaderboard_db = LeaderboardDB()
except Exception as e:
    print(f"Database initialization error: {e}")
    leaderboard_db = None

@app.route('/')
def home():
    try:
        return jsonify({"message": "Hello from Flask!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/games')
def level():
    try:
        return render_template('game-index.html')
    except Exception as e:
        return jsonify({"error": f"Template error: {str(e)}"}), 500

@app.route('/level')
def game_no():
    try:
        return render_template('game-no.html')
    except Exception as e:
        return jsonify({"error": f"Template error: {str(e)}"}), 500

@app.route('/card-match')
def card_match():
    try:
        return render_template('game-pic.html')
    except Exception as e:
        return jsonify({"error": f"Template error: {str(e)}"}), 500

@app.route('/submit_picture_score', methods=['POST'])
def submit_picture_score():
    try:
        if not leaderboard_db:
            return jsonify({"error": "Database not initialized"}), 500
        data = request.get_json()
        username = data['username']
        completion_time = data['completion_time']
        moves = data['moves']
        leaderboard_db.add_picture_game_score(username, completion_time, moves)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error in submit_picture_score: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/leaderboard')
def leaderboard():
    try:
        if not leaderboard_db:
            return jsonify({"error": "Database not initialized"}), 500
        top_players = leaderboard_db.get_top_players()
        picture_top_players = leaderboard_db.get_top_picture_players()
        return render_template('leaderboard.html', 
                             top_players=top_players,
                             picture_top_players=picture_top_players)
    except Exception as e:
        return jsonify({"error": f"Leaderboard error: {str(e)}"}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"message": "Hello from Flask!"})

# Add this for Vercel serverless
app.debug = True

# This is important for Vercel
if __name__ == '__main__':
    app.run()
# Add this for Vercel
# app = app
