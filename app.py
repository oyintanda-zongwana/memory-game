from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/level')
def level():
    return render_template('game.html')

@app.route('/nav')
def nav():
    return render_template('navbar.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
