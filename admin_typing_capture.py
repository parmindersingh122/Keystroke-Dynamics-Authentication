# -*- coding: utf-8 -*-
import csv
import time
from pynput import keyboard
import sys
import os

# Fix encoding issues
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

typed_data = []
key_down_times = {}
prev_key_time = None

# === Settings ===
guided_sentences = [
    "Security starts with trust",
    "Typing is your new password",
    "I am the only authorized user"
]
output_file = "typing_data.csv"

def on_press(key):
    global prev_key_time

    try:
        char = key.char
    except AttributeError:
        return  # Skip special keys like Shift, Ctrl

    press_time = time.time()
    key_down_times[char] = press_time

    delay = 0 if prev_key_time is None else round(press_time - prev_key_time, 4)
    prev_key_time = press_time

    typed_data.append({
        "Character": char,
        "PressTime": press_time,
        "Delay": delay  # HoldTime added on release
    })

def on_release(key):
    try:
        char = key.char
    except AttributeError:
        return

    release_time = time.time()
    for row in reversed(typed_data):
        if row["Character"] == char and "ReleaseTime" not in row:
            row["ReleaseTime"] = release_time
            row["HoldTime"] = round(release_time - row["PressTime"], 4)
            break

def capture_typing(sentence):
    global typed_data, prev_key_time, key_down_times
    typed_data = []
    prev_key_time = None
    key_down_times = {}

    print(f"\n-> Type this exact sentence:\n\"{sentence}\"\n(Press Enter when done)\n")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        user_input = input("Your input: ").strip()
        listener.stop()

    if user_input != sentence:
        print("X Input didn't match. Please try again.\n")
        return capture_typing(sentence)

def save_to_csv(label):
    with open(output_file, "a", newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Key", "PressTime", "ReleaseTime", "Delay", "HoldTime", "Character", "Label"])
        for row in typed_data:
            if "ReleaseTime" in row:  # skip incomplete
                writer.writerow([
                    row["Character"].upper(),
                    row["PressTime"],
                    row["ReleaseTime"],
                    row["Delay"],
                    row["HoldTime"],
                    row["Character"],
                    label
                ])
        # mark session end
        writer.writerow(["SESSION_END", "", "", "", "", "", label])

if __name__ == "__main__":
    print("\nWelcome to NITRO 4 UPGRADED - Admin Typing Capture\n")

    for sentence in guided_sentences:
        capture_typing(sentence)

    while True:
        name = input("\nDone! Enter your name: ").strip()
        if name:
            break
        print("Name cannot be empty. Try again.")

    save_to_csv(name)
    print(f"\nTyping data saved to {output_file} for user: {name}")