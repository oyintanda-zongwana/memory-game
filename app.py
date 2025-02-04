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

@app.route('/', methods=['GET'])
def home():
    try:
        # Print debug information to trace path and check file
        print("Attempting to render index.html")
        template_dir = os.path.join(os.getcwd(), 'templates')  # Make sure 'templates' is in the right place
        template_path = os.path.join(template_dir, 'index.html')

        print(f"Template directory: {template_dir}")
        print(f"Template path: {template_path}")
        
        # Ensure the template exists
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template 'index.html' not found at {template_path}")
        
        # Use Flask's render_template to serve the template
        return render_template('index.html')
    
    except Exception as e:
        print(f"Error in route: {str(e)}")
        # Provide details of the issue in the JSON response
        dir_contents = os.listdir(template_dir) if os.path.exists(template_dir) else []
        
        return jsonify({
            "error": str(e),
            "details": {
                "cwd": os.getcwd(),
                "template_dir_exists": os.path.exists(template_dir),
                "template_file_exists": os.path.exists(template_path),
                "dir_contents": dir_contents
            }
        }), 500  

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

@app.route('/debug')
def debug():
    template_dir = os.path.join(os.getcwd(), 'templates')
    if os.path.exists(template_dir):
        files = os.listdir(template_dir)
        return jsonify({
            "template_dir_exists": True,
            "files_in_template_dir": files
        })
    else:
        return jsonify({
            "template_dir_exists": False
        })  

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({"message": "Hello from Flask!"})

# Add this for Vercel serverless
app.debug = True

# This is important for Vercel
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
# Add this for Vercel
# app = app
