# app.py
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "success", "message": "Flask API is running"})

# Vercel requires this
if __name__ == '__main__':
    app.run()