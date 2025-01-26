# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from database_handler import LeaderboardDB

app = Flask(__name__)
CORS(app)
leaderboard_db = LeaderboardDB()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/level')
def level():
    return render_template('game.html')

@app.route('/leaderboard')
def leaderboard():
    top_players = leaderboard_db.get_top_players()
    return render_template('leaderboard.html', top_players=top_players)

@app.route('/submit_score', methods=['POST'])
def submit_score():
    try:
        data = request.get_json()
        print("Received data:", data)  # Add this debug line
        username = data['username']
        score = data['score'].split(',')
        total_time = float(score[0])
        total_moves = int(score[1])
        leaderboard_db.add_score(username, total_time, total_moves)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error in submit_score: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

# Add this for Vercel
# app = app