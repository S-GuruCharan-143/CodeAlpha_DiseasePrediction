"""
Generate a representative German Credit Dataset CSV.

Creates a realistic synthetic dataset with 1000 rows matching
the schema and distributions of the original German Credit Dataset.
"""

import csv
import random
import os

random.seed(42)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "datasets", "german_credit_data.csv")

NUM_ROWS = 1000

# --- Distribution definitions ---
SEXES = ["male", "female"]
SEX_WEIGHTS = [0.69, 0.31]

JOBS = [0, 1, 2, 3]
JOB_WEIGHTS = [0.07, 0.20, 0.63, 0.10]

HOUSING_OPTIONS = ["own", "rent", "free"]
HOUSING_WEIGHTS = [0.71, 0.18, 0.11]

SAVING_OPTIONS = ["little", "moderate", "quite rich", "rich", None]
SAVING_WEIGHTS = [0.40, 0.10, 0.06, 0.05, 0.39]

CHECKING_OPTIONS = ["little", "moderate", "rich", None]
CHECKING_WEIGHTS = [0.27, 0.17, 0.06, 0.50]

PURPOSES = [
    "car",
    "furniture/equipment",
    "radio/TV",
    "domestic appliances",
    "repairs",
    "education",
    "business",
    "vacation/others",
]
PURPOSE_WEIGHTS = [0.34, 0.18, 0.28, 0.01, 0.02, 0.05, 0.09, 0.03]

RISK_OPTIONS = ["good", "bad"]
RISK_WEIGHTS = [0.70, 0.30]


def weighted_choice(options, weights):
    """Pick a random item from options using the given weight distribution."""
    return random.choices(options, weights=weights, k=1)[0]


def generate_row():
    """Generate a single row of synthetic credit data."""
    age = random.randint(18, 75)
    sex = weighted_choice(SEXES, SEX_WEIGHTS)
    job = weighted_choice(JOBS, JOB_WEIGHTS)
    housing = weighted_choice(HOUSING_OPTIONS, HOUSING_WEIGHTS)
    saving = weighted_choice(SAVING_OPTIONS, SAVING_WEIGHTS)
    checking = weighted_choice(CHECKING_OPTIONS, CHECKING_WEIGHTS)

    # Credit amount: right-skewed distribution (log-normal-like)
    credit_amount = int(random.lognormvariate(7.8, 0.8))
    credit_amount = max(250, min(credit_amount, 20000))

    # Duration: typically 6–72 months, skewed towards shorter durations
    duration = random.choice(
        [4, 6, 9, 10, 12, 15, 18, 21, 24, 27, 30, 33, 36, 42, 48, 54, 60, 72]
    )

    purpose = weighted_choice(PURPOSES, PURPOSE_WEIGHTS)

    # Risk correlates somewhat with credit amount, duration, and savings
    bad_risk_prob = 0.30
    if credit_amount > 10000:
        bad_risk_prob += 0.10
    if duration > 36:
        bad_risk_prob += 0.10
    if saving is None or saving == "little":
        bad_risk_prob += 0.05
    if checking is None:
        bad_risk_prob += 0.03
    if age < 25:
        bad_risk_prob += 0.05
    if job <= 1:
        bad_risk_prob += 0.03

    # Clamp probability
    bad_risk_prob = min(bad_risk_prob, 0.85)
    risk = "bad" if random.random() < bad_risk_prob else "good"

    return {
        "Age": age,
        "Sex": sex,
        "Job": job,
        "Housing": housing,
        "Saving accounts": saving if saving is not None else "",
        "Checking account": checking if checking is not None else "",
        "Credit amount": credit_amount,
        "Duration": duration,
        "Purpose": purpose,
        "Risk": risk,
    }


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    fieldnames = [
        "Age",
        "Sex",
        "Job",
        "Housing",
        "Saving accounts",
        "Checking account",
        "Credit amount",
        "Duration",
        "Purpose",
        "Risk",
    ]

    rows = [generate_row() for _ in range(NUM_ROWS)]

    # Print distribution summary
    risk_counts = {"good": 0, "bad": 0}
    for r in rows:
        risk_counts[r["Risk"]] += 1
    print(f"Generated {NUM_ROWS} rows")
    print(f"Risk distribution: good={risk_counts['good']}, bad={risk_counts['bad']}")
    print(f"  good: {risk_counts['good']/NUM_ROWS*100:.1f}%")
    print(f"  bad:  {risk_counts['bad']/NUM_ROWS*100:.1f}%")

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDataset saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
