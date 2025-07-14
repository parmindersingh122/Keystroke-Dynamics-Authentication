# -*- coding: utf-8 -*-
import time, json, joblib, pandas as pd
import sys
import os

# Fix encoding issues
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

# Configuration
TEST_SENTENCE = "Security starts with trust"
TOTAL_KEYS = len(TEST_SENTENCE)

def capture_test():
    print(f'\nType exactly:\n"{TEST_SENTENCE}"')
    typed = input("\nYour input (type the full sentence, then ENTER): ").strip()

    # sentence mismatch diagnostics
    if typed != TEST_SENTENCE:
        print("\nX Sentence mismatch.")
        print(f'   You typed : "{typed}"   (length {len(typed)})')
        print(f'   Expected  : "{TEST_SENTENCE}"   (length {TOTAL_KEYS})')
        return None

    print(f"\nNow press ENTER for each of the {TOTAL_KEYS} characters.")
    rows, prev_time = [], None
    for idx, ch in enumerate(TEST_SENTENCE, start=1):
        input(f"[{idx:>2}/{TOTAL_KEYS}] Press: {ch} ")
        t0 = time.time()
        hold = 0.15 + 0.05 * (ord(ch.lower()) % 3)  # simulated hold
        delay = 0 if prev_time is None else round(t0 - prev_time, 4)
        rows.append({"HoldTime": hold, "Delay": delay})
        prev_time = t0

    if len(rows) != TOTAL_KEYS:
        print("Internal count mismatch - aborted.")
        return None
    return pd.DataFrame(rows)

def to_feature_row(df: pd.DataFrame) -> dict:
    return {
        "mean_hold": df["HoldTime"].mean(),
        "std_hold": df["HoldTime"].std(),
        "mean_delay": df["Delay"].mean(),
        "std_delay": df["Delay"].std(),
        "iqr_hold": df["HoldTime"].quantile(0.75) - df["HoldTime"].quantile(0.25),
        "iqr_delay": df["Delay"].quantile(0.75) - df["Delay"].quantile(0.25),
    }

def authenticate():
    sample_df = capture_test()
    if sample_df is None:
        return

    try:
        clf = joblib.load("typing_model.pkl")
        with open("typing_meta.json", 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except FileNotFoundError:
        print("X Model not found - run option 2 (train) first.")
        return

    X = pd.DataFrame([to_feature_row(sample_df)])[meta["columns"]]
    verdict = clf.predict(X)[0]  # 1 = admin-like, -1 = outlier

    if verdict == 1:
        print(f"\n✓ Access Granted - Welcome, {meta['admin_name'].title()}!")
    else:
        print("\nX Access Denied - Typing pattern not recognized.")

if __name__ == "__main__":
    authenticate()