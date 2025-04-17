from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
import tempfile
import os
import requests
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF

app = Flask(__name__)
# allows requests from frontend
CORS(app)

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    try:
        body = request.get_json(force=True)
        pdf_url = body.get('pdfUrl')
        if not pdf_url:
            return {"error":"Missing pdfUrl"}, 400
        resp = requests.get(pdf_url); resp.raise_for_status()
        src = BytesIO(resp.content)

        # 2) read & copy pages
        reader = PdfReader(src)
        if not reader.pages:
            return {"error":"No pages in PDF"}, 400
        writer = PdfWriter()
        for p in reader.pages:
            writer.add_page(p)

        # 3) generate + append FPDF page
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=24)
        pdf.cell(0, 10, txt="Your text here", ln=True, align='C') #FIXME update prompt
        raw = pdf.output(dest='S').encode('latin-1')
        new_page = PdfReader(BytesIO(raw)).pages[0]
        writer.add_page(new_page)

        # 4) dump merged PDF to buffer
        out_buf = BytesIO()
        writer.write(out_buf)
        out_buf.seek(0)
        with open("merged_test.pdf", "wb") as f_out:
            # Tell PyPDF2 to write its contents there
            writer.write(f_out) #FIXME testing
        pdf_bytes = out_buf.getvalue()

        # 5) call your LLM
        result = call_llm_api(pdf_bytes)  # or pdf_bytes

        # 6) return LLM answer
        return {"result": result}, 200

    except Exception as e:
        app.logger.exception("PDF processing failed")
        return {"error": str(e)}, 500

def call_llm_api(pdf_content):
    # FIXME Replace with your actual LLM API call
    return "Sample analysis result"

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
