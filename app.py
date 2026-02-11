from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from models import db, Entry
import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Ensure DB file exists
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    entries = Entry.query.all()
    return render_template("index.html", entries=entries)

@app.route('/add', methods=["POST"])
def add_entry():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("All fields are required!", "danger")
        return redirect(url_for("home"))

    entry = Entry(name=name, email=email, message=message)
    db.session.add(entry)
    db.session.commit()
    flash("Entry added successfully!", "success")
    return redirect(url_for("home"))

@app.route('/api/entries')
def api_entries():
    data = [
        {"id": e.id, "name": e.name, "email": e.email, "message": e.message}
        for e in Entry.query.all()
    ]
    return jsonify({"entries": data, "status": "running", "time": datetime.datetime.now().isoformat()})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# Remove debug=True for EB
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
