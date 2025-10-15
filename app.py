from flask import Flask, render_template, jsonify
import logging
import socket
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, filename="app_errors.log", format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize state
emotion_state = {
    "emotion": None,
    "logs": []
}

@app.route('/')
def index():
    try:
        logger.info("Serving index page")
        print("Serving index page")
        return render_template('index.html', emotion=emotion_state["emotion"])
    except Exception as e:
        logger.error("Error serving index: %s", e)
        print(f"Error serving index: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    logger.info("Health check requested")
    print("Health check requested")
    return jsonify({"status": "running", "logs": emotion_state["logs"]})

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5000))
    logger.info("Starting Flask server on port %s", port)
    print(f"Starting Flask server on port {port}")
    if is_port_in_use(port):
        logger.error("Port %s is already in use", port)
        print(f"Port {port} is in use. Please free it or set a different port via FLASK_PORT environment variable.")
        sys.exit(1)
    try:
        app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
    except Exception as e:
        logger.error("Server error: %s", e)
        print(f"Server error: {e}")