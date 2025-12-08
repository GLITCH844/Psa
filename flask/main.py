from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Blacklist dictionary
COMMON_WORDS = [
    "password", "admin", "welcome", "qwerty",
    "abc123", "letmein", "custech",
    "24L!CY", "UG1234", "school"
]

def contains_dictionary_word(password):
    password = password.lower()
    
    for word in COMMON_WORDS:
        if word in password:
            return word   # RETURN THE MATCHED WORD
            
    return None

def analyze_password(password):

    matched_word = contains_dictionary_word(password)

    rules = {
        "Length ≥ 8": len(password) >= 8,
        "Contains lowercase": bool(re.search(r"[a-z]", password)),
        "Contains uppercase": bool(re.search(r"[A-Z]", password)),
        "Contains number": bool(re.search(r"\d", password)),
        "Contains special symbol": bool(re.search(r"[^A-Za-z0-9]", password)),
        "No common/predictable words": matched_word is None
    }

    score = sum(rules.values())
    total_rules = len(rules)

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    percent = int((score / total_rules) * 100)

    warning = None
    if matched_word:
        warning = f"⚠ Predictable password detected: '{matched_word}'"

    return strength, percent, warning, rules

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():

    data = request.get_json()
    password = data.get("password", "")

    strength, percent, warning, rules = analyze_password(password)

    return jsonify({
        "strength": strength,
        "percent": percent,
        "warning": warning,
        "rules": rules
    })

if __name__ == "__main__":
    app.run(debug=True)