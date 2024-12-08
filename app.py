import os
import subprocess
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/run-command/", methods=["POST"])
def run_command():
    try:
        # Ambil command dari body request
        data = request.get_json()
        command = data.get("command")
        if not command:
            return jsonify({"error": "Command not provided"}), 400

        # Jalankan perintah shell dan tangkap outputnya
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return jsonify({"output": result})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Command failed: {e.output}"}), 400
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
