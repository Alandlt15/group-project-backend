from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import tempfile
import os

app = Flask(__name__)
# allows requests from frontend
CORS(app) 

# runs the default houyi attack
@app.route('/attack', methods=['POST'])
def default_attack():
    try:
        # runs main.py using subprocess
        result = subprocess.run([sys.executable, "main.py"], capture_output=True, text=True, check=True)
        # returns logs in json
        return jsonify({
            "status": "success",
            "output": result.stdout
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "output": e.stderr
        }), 500
    
# runs the custom attack
@app.route('/custom_attack', methods=['POST'])
def custom_attack():

    # gets newly written harness and attack intentions
    intention_path = "intention/custom_intention.py"
    harness_path = "harness/custom_harness.py"
    try:
        # runs custom_main.py using subprocess
        result = subprocess.run(
            [sys.executable, "custom_main.py", harness_path, intention_path],
            capture_output=True, text=True, check=True
        )
        # returns logs in json
        return jsonify({
            "status": "success",
            "output": result.stdout
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            "status": "error",
            "output": e.stderr
        }), 500

# creates a harness and attack with user input from the frontend
@app.route('/create_attack', methods=['POST'])
def create_attack():
    try:
        # gets data from request
        data = request.get_json()
        intention_code = data['intentionCode']
        harness_code = data['harnessCode']

        # gets paths to write back to them
        intention_path = "intention/custom_intention.py"
        harness_path = "harness/custom_harness.py"

        # Write code to these files
        with open(intention_path, 'w') as f:
            f.write(intention_code)
            print("[+] Wrote intention code to custom_intention.py")

        with open(harness_path, 'w') as f:
            f.write(harness_code)
            print("[+] Wrote harness code to custom_harness.py")

        # returns 200 
        return jsonify({
            "status": "success",
            "output": "[+] Custom files written successfully."
        })

    except Exception as e:
        print("[-] General exception:", str(e))
        return jsonify({
            "status": "error",
            "output": str(e)
        }), 500

# starts the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
