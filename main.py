import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def show_menu():
    clear()
    print("\n🔐 WELCOME TO NITRO 4 UPGRADED")
    print("-" * 34)
    print("1️⃣  Record Admin Typing")
    print("2️⃣  Train Authentication Model")
    print("3️⃣  Test Current User")
    print("4️⃣  Exit")
    print("-" * 34)

def main():
    while True:
        show_menu()
        choice = input("👉 Enter your choice (1-4): ").strip()

        if choice == '1':
            os.system("python admin_typing_capture.py")
            input("\n🔁 Press ENTER to return to the menu...")

        elif choice == '2':
            os.system("python train_user_model.py")
            input("\n🔁 Press ENTER to return to the menu...")

        elif choice == '3':
            os.system("python live_user_cheak.py")  # ✅ fixed filename typo
            input("\n🔁 Press ENTER to return to the menu...")

        elif choice == '4':
            print("👋 Exiting... Goodbye!")
            break

        else:
            print("❗ Invalid choice. Try again.")
            input("🔁 Press ENTER to continue...")

if __name__ == "__main__":
    main()
