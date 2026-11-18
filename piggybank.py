import tkinter as tk
from tkinter import messagebox
import os
import sys
import json
import base64
import hashlib

# Secret key for encrypting and verifying saved data
SECRET_KEY = "MySuperSecretPiggyKey2026!"
INITIAL_BAL = 0.00

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_save_file_path():
    """ Store save file safely in Windows Local AppData folder """
    app_data = os.getenv('LOCALAPPDATA') or os.path.expanduser("~")
    folder = os.path.join(app_data, "KidsPiggyBank")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "piggy_data.dat")

def encrypt_and_save(balance):
    """ Encrypts the balance and signs it with SHA-256 so it cannot be tampered with """
    raw_data = f"{balance:.2f}"
    # Generate tamper-proof signature
    signature = hashlib.sha256((raw_data + SECRET_KEY).encode()).hexdigest()
    payload = json.dumps({"bal": raw_data, "sig": signature}).encode()
    
    # Scramble bytes using SECRET_KEY
    key_bytes = SECRET_KEY.encode()
    scrambled = bytes([payload[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(payload))])
    encoded = base64.b64encode(scrambled)
    
    with open(get_save_file_path(), "wb") as f:
        f.write(encoded)

def load_and_decrypt():
    """ Reads and decrypts the saved balance; returns {INITIAL_BAL} if missing or tampered """
    file_path = get_save_file_path()
    if not os.path.exists(file_path):
        return INITIAL_BAL
    
    try:
        with open(file_path, "rb") as f:
            encoded = f.read()
        
        scrambled = base64.b64decode(encoded)
        key_bytes = SECRET_KEY.encode()
        payload = bytes([scrambled[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(scrambled))])
        
        data = json.loads(payload.decode())
        raw_data = data["bal"]
        signature = data["sig"]
        
        # Verify signature to prevent manual editing
        expected_sig = hashlib.sha256((raw_data + SECRET_KEY).encode()).hexdigest()
        if signature == expected_sig:
            return float(raw_data)
        else:
            messagebox.showwarning("Security Alert", f"Save file was modified! Resetting to ₹{INITIAL_BAL:,.2f}.")
            return 5000.00
    except Exception:
        return 5000.00

class KidsPiggyBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Piggy Bank")
        self.root.geometry("400x460")
        self.root.configure(bg="#FFF8E7")

        # Set Window Titlebar Icon safely
        icon_path = get_resource_path("piggy.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        # Load saved encrypted balance
        self.balance = load_and_decrypt()

        # Title Banner
        self.title_label = tk.Label(
            root, text="🐷 My Piggy Bank 🐷", 
            font=("Comic Sans MS", 20, "bold"), 
            bg="#FFCC00", fg="#333333", pady=10
        )
        self.title_label.pack(fill="x")

        # Balance Display
        self.balance_label = tk.Label(
            root, text=f"Balance: ₹{self.balance:,.2f}", 
            font=("Arial", 18, "bold"), 
            bg="#FFF8E7", fg="#2E7D32", pady=20
        )
        self.balance_label.pack()

        # Input Instruction
        self.prompt_label = tk.Label(
            root, text="Enter Amount (₹):", 
            font=("Arial", 12), bg="#FFF8E7"
        )
        self.prompt_label.pack()

        # Amount Entry Box
        self.amount_entry = tk.Entry(root, font=("Arial", 16), justify="center", width=15)
        self.amount_entry.pack(pady=10)

        # Deposit Button
        self.deposit_btn = tk.Button(
            root, text="➕ Add Money (Deposit)", 
            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
            width=22, pady=8, command=self.deposit_money
        )
        self.deposit_btn.pack(pady=8)

        # Withdraw Button
        self.withdraw_btn = tk.Button(
            root, text="➖ Spend Money (Withdraw)", 
            font=("Arial", 12, "bold"), bg="#FF7043", fg="white", 
            width=22, pady=8, command=self.withdraw_money
        )
        self.withdraw_btn.pack(pady=8)

        # Exit Button
        self.exit_btn = tk.Button(
            root, text="🚪 Save & Close", 
            font=("Arial", 11), bg="#9E9E9E", fg="white", 
            width=18, pady=5, command=root.quit
        )
        self.exit_btn.pack(pady=20)

    def update_balance_display(self):
        self.balance_label.config(text=f"Balance: ₹{self.balance:,.2f}")
        self.amount_entry.delete(0, tk.END)
        # Encrypt and save immediately after every transaction
        encrypt_and_save(self.balance)

    def deposit_money(self):
        try:
            amount = float(self.amount_entry.get())
            if amount > 0:
                self.balance += amount
                self.update_balance_display()
                messagebox.showinfo("Yay!", f"Great job! You added ₹{amount:,.2f} to your Piggy Bank!")
            else:
                messagebox.showwarning("Oops!", "Please enter an amount bigger than ₹0.")
        except ValueError:
            messagebox.showerror("Error", "Please type numbers only!")

    def withdraw_money(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showwarning("Oops!", "Please enter an amount bigger than ₹0.")
            elif amount > self.balance:
                messagebox.showwarning("Not Enough Money!", "You don't have enough savings for that yet!")
            else:
                self.balance -= amount
                self.update_balance_display()
                messagebox.showinfo("Spent!", f"You took out ₹{amount:,.2f}.")
        except ValueError:
            messagebox.showerror("Error", "Please type numbers only!")

if __name__ == "__main__":
    root = tk.Tk()
    app = KidsPiggyBankApp(root)
    root.mainloop()
