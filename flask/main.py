from flask import Flask, render_template, request
import re

app = Flask(_name_)

def check_strength(password):
    score = 0
    rules = {
        "Length at least 8": len(password) >= 8,
        "Contains lowercase": bool(re.search(r"[a-z]", password)),
        "Contains uppercase": bool(re.search(r"[A-Z]", password)),
        "Contains digits": bool(re.search(r"[0-9]", password)),
        "Contains special characters": bool(re.search(r"[^A-Za-z0-9]", password))
    }

    for rule, passed in rules.items():
        if passed:
            score += 1

    if score <= 2:
        strength = "Weak"
    elif score == 3 or score == 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, rules

@app.route("/", methods=["GET", "POST"])
def index():
    strength = None
    rules = None

    if request.method == "POST":
        password = request.form["password"]
        strength, rules = check_strength(password)

    return render_template("index.html", strength=strength, rules=rules)

if _name_ == "_main_":
    app.run(debug=True)