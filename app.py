# app.py
from flask import Flask, render_template, request, redirect, url_for
from database_handler import LeaderboardDB

app = Flask(__name__)
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
    username = request.form['username']
    score = float(request.form['score'].split(',')[0])
    moves = int(request.form['score'].split(',')[1])
    leaderboard_db.add_score(username, score, moves)
    return redirect(url_for('leaderboard'))

if __name__ == '__main__':
    app.run(debug=True)

# Add this for Vercel
# app = app