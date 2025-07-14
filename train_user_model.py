# -*- coding: utf-8 -*-
import pandas as pd
import json
import joblib
import sys
import os
from sklearn.ensemble import IsolationForest

# Fix encoding issues
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

try:
    # Load data (admin only)
    df = pd.read_csv("typing_data.csv", encoding='utf-8')
    df["HoldTime"] = df["ReleaseTime"] - df["PressTime"]

    admin_name = df["Label"].value_counts().idxmax()
    df = df[df["Label"] == admin_name]

    # Slice into 25-char sessions & compute 6 features per session
    CHARS_PER_SENTENCE = 25
    sessions = []
    for i in range(0, len(df), CHARS_PER_SENTENCE):
        chunk = df.iloc[i:i+CHARS_PER_SENTENCE]
        if len(chunk) == CHARS_PER_SENTENCE:
            sessions.append({
                "mean_hold": chunk["HoldTime"].mean(),
                "std_hold": chunk["HoldTime"].std(),
                "mean_delay": chunk["Delay"].mean(),
                "std_delay": chunk["Delay"].std(),
                "iqr_hold": chunk["HoldTime"].quantile(0.75)-chunk["HoldTime"].quantile(0.25),
                "iqr_delay": chunk["Delay"].quantile(0.75)-chunk["Delay"].quantile(0.25),
            })

    X = pd.DataFrame(sessions)

    # Train Isolation Forest
    clf = IsolationForest(contamination=0.1, random_state=42)
    clf.fit(X)

    joblib.dump(clf, "typing_model.pkl")
    with open("typing_meta.json", "w", encoding='utf-8') as f:
        json.dump({"admin_name": admin_name, "columns": list(X.columns)}, f, indent=2)

    print("\n✓ Isolation-Forest model saved as typing_model.pkl")
    print(f"Authorized admin: {admin_name}")

except FileNotFoundError:
    print("X Error: typing_data.csv not found. Please run admin typing capture first.")
except Exception as e:
    print(f"X Error during training: {str(e)}")