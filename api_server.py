# api_server.py
from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import sys

app = Flask(__name__)
CORS(app)  # allow requests from your frontend

@app.route('/attack', methods=['POST'])
def attack():
    try:
        # Run main.py using subprocess
        result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True, check=True)
        return jsonify({
            "status": "success",
            "output": result.stdout
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "output": e.stderr
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
