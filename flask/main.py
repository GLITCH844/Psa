from flask import Flask, render_template, request, jsonify
import re

app = Flask(_name_)

# Simple dictionary blacklist
COMMON_WORDS = [
    "password", "admin", "welcome", "qwerty", "abc123",
    "custech", "iloveyou", "football", "monkey", "dragon"
]

def check_dictionary(password):
    password_lower = password.lower()
    for word in COMMON_WORDS:
        if word in password_lower:
            return True
    return False

def analyze_password(password):
    rules = {
        "Length ≥ 8": len(password) >= 8,
        "Contains lowercase": bool(re.search(r"[a-z]", password)),
        "Contains uppercase": bool(re.search(r"[A-Z]", password)),
        "Contains number": bool(re.search(r"\d", password)),
        "Contains special symbol": bool(re.search(r"[^A-Za-z0-9]", password)),
        "Not a dictionary word": not check_dictionary(password)
    }

    score = sum(rules.values())

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    percent = int((score / len(rules)) * 100)

    return strength, percent, rules

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    password = data.get("password")

    strength, percent, rules = analyze_password(password)

    return jsonify({
        "strength": strength,
        "percent": percent,
        "rules": rules
    })

if _name_ == "_main_":
    app.run(debug=True)