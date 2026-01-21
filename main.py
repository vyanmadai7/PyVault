import os
import json
import bcrypt
import getpass

VAULT_FILE = "vault.json"

# Create vault file if it doesn't exist
def ensure_vault_exists():
    if not os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "w") as f:
            json.dump({"master": None, "entries": []}, f)

def load_vault():
    with open(VAULT_FILE, "r") as f:
        return json.load(f)

def save_vault(data):
    with open(VAULT_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Set master password
def set_master_password():
    print("---- SET MASTER PASSWORD ----")
    while True:
        pw = getpass.getpass("Enter new password: ")
        pw2 = getpass.getpass("Confirm password: ")

        if pw != pw2:
            print("Passwords do not match.")
        elif len(pw) < 8:
            print("Password must be at least 8 characters.")
        else:
            break

    hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
    vault = load_vault()
    vault["master"] = hashed.decode("utf-8")
    save_vault(vault)
    print("Master password saved!")

# Verify master password
def verify_master_password():
    vault = load_vault()
    if not vault["master"]:
        print("No master password set.")
        return False

    pw = getpass.getpass("Enter master password: ")
    if bcrypt.checkpw(pw.encode(), vault["master"].encode()):
        return True
    else:
        print("Incorrect password!")
        return False

# Add entry
def add_entry():
    name = input("Account name: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    vault = load_vault()
    vault["entries"].append({
        "name": name,
        "username": username,
        "password": password
    })
    save_vault(vault)
    print("Entry added!")

# View entry
def get_entry():
    name = input("Account name: ")
    vault = load_vault()

    for entry in vault["entries"]:
        if entry["name"].lower() == name.lower():
            print("Username:", entry["username"])
            print("Password:", entry["password"])
            return

    print("No entry found.")

# List entries
def list_entries():
    vault = load_vault()
    if not vault["entries"]:
        print("No stored accounts.")
        return

    print("Stored accounts:")
    for e in vault["entries"]:
        print("-", e["name"])

# Delete entry
def delete_entry():
    name = input("Account name to delete: ")
    vault = load_vault()

    new_entries = [e for e in vault["entries"]
                   if e["name"].lower() != name.lower()]

    if len(new_entries) == len(vault["entries"]):
        print("No such entry.")
    else:
        vault["entries"] = new_entries
        save_vault(vault)
        print("Entry deleted!")

# Initialize
def initialize():
    ensure_vault_exists()
    vault = load_vault()
    if not vault["master"]:
        set_master_password()

# Menu
def menu():
    initialize()

    while True:
        print("\n---- PASSWORD MANAGER ----")
        print("1. Add account")
        print("2. View account")
        print("3. List accounts")
        print("4. Delete account")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            if verify_master_password(): add_entry()
        elif choice == "2":
            if verify_master_password(): get_entry()
        elif choice == "3":
            if verify_master_password(): list_entries()
        elif choice == "4":
            if verify_master_password(): delete_entry()
        elif choice == "0":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()
