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

@app.route('/games')
def level():
    return render_template('game-index.html')

@app.route('/level')
def game_no():
    return render_template('game-no.html')

@app.route('/card-match')
def card_match():
    return render_template('game-pic.html')

@app.route('/submit_picture_score', methods=['POST'])
def submit_picture_score():
    try:
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
    top_players = leaderboard_db.get_top_players()
    picture_top_players = leaderboard_db.get_top_picture_players()
    return render_template('leaderboard.html', 
                         top_players=top_players,
                         picture_top_players=picture_top_players)


if __name__ == '__main__':
    app.run(debug=True)

# Add this for Vercel
# app = app