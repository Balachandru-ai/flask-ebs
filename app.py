from flask import Flask, jsonify, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/api')
def api():
    return jsonify({
        "message": "Flask CI/CD with Elastic Beanstalk 🚀",
        "status": "running",
        "time": datetime.datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run()
