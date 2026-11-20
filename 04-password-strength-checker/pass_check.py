#!/usr/bin/env python3
"""Evaluate password entropy and basic policy checks."""

import argparse
import math
import re

COMMON_WEAK = {"password", "123456", "12345678", "qwerty", "admin", "letmein", "welcome", "iloveyou"}


def calculate_entropy(password: str) -> float:
    if not password:
        return 0.0
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        pool += 32
    if pool == 0:
        return 0.0
    return round(len(password) * math.log2(pool), 2)


def evaluate(password: str) -> dict:
    entropy = calculate_entropy(password)
    issues = []
    if len(password) < 12:
        issues.append("Length is under 12 characters")
    if not re.search(r"[a-z]", password):
        issues.append("Missing lowercase letter")
    if not re.search(r"[A-Z]", password):
        issues.append("Missing uppercase letter")
    if not re.search(r"\d", password):
        issues.append("Missing digit")
    if not re.search(r"[^a-zA-Z0-9]", password):
        issues.append("Missing special symbol")
    if password.lower() in COMMON_WEAK or any(w in password.lower() for w in COMMON_WEAK):
        issues.append("Contains a common weak word/sequence")

    if entropy >= 75 and not issues:
        rating = "Strong"
    elif entropy >= 50 and len(issues) <= 1:
        rating = "Moderate"
    else:
        rating = "Weak"

    return {"length": len(password), "entropy_bits": entropy, "rating": rating, "issues": issues}


def main() -> None:
    parser = argparse.ArgumentParser(description="Password Entropy & Policy Checker")
    parser.add_argument("password", help="Password string to evaluate")
    args = parser.parse_args()

    res = evaluate(args.password)
    print(f"Length:       {res['length']}")
    print(f"Est. Entropy: {res['entropy_bits']} bits")
    print(f"Rating:       {res['rating']}")
    if res["issues"]:
        print("Suggestions:")
        for item in res["issues"]:
            print(f"  - {item}")
    else:
        print("Suggestions:  None — meets baseline checks.")


if __name__ == "__main__":
    main()
