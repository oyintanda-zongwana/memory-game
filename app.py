# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from database_handler import LeaderboardDB

# Print current directory for debugging
print("Current working directory:", os.getcwd())

app = Flask(__name__, 
    static_folder='static',
    template_folder='templates'
) 
CORS(app)

# Print template folder location
print("Template folder:", app.template_folder)
if os.path.exists(app.template_folder):
    print("Templates found:", os.listdir(app.template_folder))
else:
    print("Template folder not found!")

# Initialize database only if needed
try:
    leaderboard_db = LeaderboardDB()
except Exception as e:
    print(f"Database initialization error: {e}")
    leaderboard_db = None

@app.route('/')
def home():
    try:
        template_path = os.path.join(app.template_folder, 'index.html')
        print(f"Trying to load template from: {template_path}")
        print(f"Template exists: {os.path.exists(template_path)}")
        return render_template('index.html')
    except Exception as e:
        print(f"Home route error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/games')
def level():
    try:
        template_path = os.path.join(app.template_folder, 'game-index.html')
        print(f"Trying to load template from: {template_path}")
        print(f"Template exists: {os.path.exists(template_path)}")
        return render_template('game-index.html')
    except Exception as e:
        print(f"Games route error: {str(e)}")
        return jsonify({"error": f"Template error: {str(e)}"}), 500

@app.route('/level')
def game_no():
    try:
        return render_template('game-no.html')
    except Exception as e:
        print(f"Level route error: {str(e)}")
        return jsonify({"error": f"Template error: {str(e)}"}), 500

@app.route('/card-match')
def card_match():
    try:
        return render_template('game-pic.html')
    except Exception as e:
        print(f"Card match route error: {str(e)}")
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
