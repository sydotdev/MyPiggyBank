# 🐷 My Piggy Bank (Kids Banking App)

A simple, kid-friendly desktop banking application built with Python and Tkinter. Designed to teach children basic money management—saving, spending, and checking balances—while keeping their saved pocket money safe with built-in encryption.

---

## ✨ Features

* **Kid-Friendly Interface:** Colorful, easy-to-read graphical window with large buttons and cheerful pop-up messages.
* **Deposit & Withdraw Logic:** Add pocket money or spend savings with automatic overdraft protection so balances never drop below ₹0.00.
* **Tamper-Proof Encrypted Storage:** Automatically encrypts the latest balance (`XOR` cipher + `Base64`) and verifies it with a **SHA-256 signature** in `%LOCALAPPDATA%\KidsPiggyBank\piggy_data.dat`. If the save file is manually edited or corrupted, the app alerts the user and safely resets to the initial balance (`₹5,000.00`).
* **Zero External Dependencies:** Built entirely with Python's standard library (`tkinter`, `hashlib`, `base64`, `json`, `os`).

---

## 📁 Project Structure

```text
KidsPiggyBank/
├── piggybank.py       # Main Python application source code
├── piggy.ico          # Custom application icon
├── version.txt        # Windows executable metadata (author, version, copyright)
└── README.md          # Project documentation
```

---

## 🚀 How to Run from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd KidsPiggyBank
   ```

2. **Run the application:**
   ```bash
   python piggybank.py
   ```
   *(Tip: Rename `piggybank.py` to `piggybank.pyw` on Windows to launch the app without a background console window.)*

---

## 📦 Building the Windows Executable (`.exe`)

To package the app into a standalone Windows `.exe` file with a custom icon and author details:

1. **Install PyInstaller:**
   ```bash
   python -m pip install pyinstaller
   ```

2. **Build the executable:**
   ```bash
   python -m PyInstaller --onefile --windowed --icon=piggy.ico --add-data "piggy.ico;." --version-file=version.txt --name="MyPiggyBank" piggybank.py
   ```

3. **Locate your app:**
   Find the generated **`MyPiggyBank.exe`** inside the newly created `dist/` folder.

> **Note for Windows 11 Users:** Because newly built `.exe` files are unsigned, **Windows Smart App Control** may block them from launching. On a personal PC, you can allow unsigned builds via **Windows Security > App & browser control > Smart App Control settings**.

---

## ⚙️ Configuration

You can customize the starting amount and encryption key at the top of `piggybank.py`:

```python
SECRET_KEY = "MySuperSecretPiggyKey2026!"
INITIAL_BAL = 0.00
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
