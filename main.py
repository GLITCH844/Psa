import re

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


password = input("Enter password: ")

strength, rule_results = check_strength(password)

print("\nPassword Strength:", strength)
print("\nRule Breakdown:")
for rule, passed in rule_results.items():
    print(f"{rule}: {'✔' if passed else '❌'}")