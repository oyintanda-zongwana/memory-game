# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from database_handler import LeaderboardDB

# Print current directory for debugging
print("Current working directory:", os.getcwd())

app = Flask(__name__, 
    static_folder='static',
    template_folder='templates'  # Match your actual folder name case
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

# Get the absolute path to the templates directory
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

@app.route('/', methods=['GET'])
def home():
    try:
        # Try to read the template file directly
        template_path = os.path.join(TEMPLATE_DIR, 'index.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({
            "error": str(e),
            "details": {
                "cwd": os.getcwd(),
                "template_dir": TEMPLATE_DIR,
                "template_exists": os.path.exists(TEMPLATE_DIR),
                "files": os.listdir(os.getcwd()) if os.path.exists(os.getcwd()) else [],
                "template_files": os.listdir(TEMPLATE_DIR) if os.path.exists(TEMPLATE_DIR) else []
            }
        }), 500

@app.route('/games')
def level():
    try:
        template_path = os.path.join(TEMPLATE_DIR, 'game-index.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/level')
def game_no():
    try:
        template_path = os.path.join(TEMPLATE_DIR, 'game-no.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/card-match')
def card_match():
    try:
        template_path = os.path.join(TEMPLATE_DIR, 'game-pic.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Add this for Vercel serverless
app.debug = True

# This is important for Vercel
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
# Add this for Vercel
# app = app
