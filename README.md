<div align="center">

# 🏦 Python Bank ATM

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.x-00D4FF?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Built--in-F29111?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-8B5CF6?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A professional dark-themed ATM desktop application built with Python and CustomTkinter.**  
Simulates a real banking experience — PIN authentication, deposits, withdrawals, balance privacy, and live transaction history.

[✨ Features](#-features) • [📸 Preview](#-preview) • [🚀 Quick Start](#-quick-start) • [🎮 Usage](#-usage) • [🏗️ Architecture](#%EF%B8%8F-architecture) • [🗺️ Roadmap](#%EF%B8%8F-roadmap)

</div>

---

✨ Features

 🔐 Security
| Feature | Details |
|---------|---------|
| PIN Authentication | 4-digit PIN entry with a physical numpad UI |
| Masked Input | Digits display as ● bullets — never visible as typed |
| iOS-style PIN Flash | Each digit briefly flashes for 300ms before masking |
| Balance Privacy | Balance hidden behind ₦ ● ● ● ● ● by default |
| Auto-hide Balance | Balance revealed for exactly 5 seconds then re-masked |
| Live Countdown | "Hiding in 5s…" countdown shown while balance is visible |

 💳 Banking Operations
| Feature | Details |
|---------|---------|
| Deposit | Add funds with instant balance update and confirmation |
| Withdrawal | Withdraw funds — blocked if balance is insufficient |
| Balance Enquiry | Reveals balance and starts 5-second auto-hide countdown |
| Quick-Amount Chips | One-click preset amounts: ₦500 · ₦1,000 · ₦5,000 · ₦10,000 · ₦20,000 · ₦50,000 |

 🎨 UI & Experience
| Feature | Details |
|---------|---------|
| Dark Theme | Deep navy (`#0A0E1A`) with cyan-blue (`#00D4FF`) accents |
| Live Clock | Real-time date and time display in the top bar |
| Animated Feedback | Colour-flash animations on success (green) and error (red) |
| Transaction History | Scrollable log of all session transactions with timestamps |
| Keyboard Support | Full numpad and keyboard entry — digits, Backspace, Enter |
| Logout Confirmation | Session-end dialog before returning to PIN screen |

---

## 📸 Preview

```
┌─────────────────────────────────────────┐
│  🏦  Micro-Finance BANK         🕐 12:34│
├─────────────────────────────────────────┤
│                                         │
│   AVAILABLE BALANCE          👁 Show   │
│   ₦ ● ● ● ● ●                          │
│                                         │
├─────────────────────────────────────────┤
│  TRANSACTION AMOUNT                     │
│  ₦  [ 10000.00             ]           │
│  ₦500  ₦1,000  ₦5,000  ₦10,000 ...   │
├─────────────────────────────────────────┤
│  💰 Deposit   🏧 Withdraw   📋 Balance │
├─────────────────────────────────────────┤
│  RECENT TRANSACTIONS                    │
│  [12:30:01] System   Session started   │
│  [12:31:44] Deposit  +₦10,000.00       │
│  [12:32:10] Withdraw -₦5,000.00        │
└─────────────────────────────────────────┘
```

> 📷 *Add real screenshots to `docs/screenshots/` and update the links here*

---

🚀 Quick Start

Prerequisites

- **Python 3.10** or higher
- **pip** (comes bundled with Python)

 1 · Clone

```bash
git clone https://github.com/YOUR-USERNAME/python-bank-atm.git
cd python-bank-atm
```

 2 · Create a virtual environment *(recommended)*

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

 3 · Install dependencies

```bash
pip install -r requirements.txt
```

 4 · Run

```bash
python atm.py
```
 🎮 Usage

 Logging In

1. Launch the app — the PIN screen appears automatically
2. Enter the 4-digit PIN using the on-screen numpad **or** your keyboard
3. Press **✔** or **Enter** to authenticate
4. On success the dashboard opens; on failure the entry clears with an error flash

> 🔑 **Demo PIN: `1234`**

### Making Transactions

| Action | Steps |
|--------|-------|
| **Deposit** | Type an amount (or click a chip) → click 💰 Deposit |
| **Withdrawal** | Type an amount (or click a chip) → click 🏧 Withdraw |
| **Check Balance** | Click 📋 Balance — balance reveals for 5 seconds |
| **Show/Hide Balance** | Click the 👁 Show / 🙈 Hide button on the balance card |
| **Logout** | Click ⏻ Logout → confirm in the dialog |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `0`–`9` | Enter PIN digit or amount |
| `Backspace` | Delete last PIN digit |
| `Enter` | Confirm PIN |



🏗️ Architecture

```
atm.py
│
├── flash()                  # Utility — animated colour flash on any label
│
├── class PINScreen          # Screen 1 — PIN entry & authentication
│   ├── _build()             # Constructs logo, PIN display, and numpad grid
│   ├── _key(k)              # Handles numpad button press
│   ├── _kb(event)           # Handles keyboard input
│   └── _verify()            # Validates PIN → triggers on_success callback
│
├── class DashboardScreen    # Screen 2 — Main banking interface
│   ├── _build()             # Constructs top bar, balance card, inputs, history
│   ├── _toggle_balance()    # Show / hide balance display
│   ├── _show_balance()      # Reveals balance + starts 5-second auto-hide
│   ├── _hide_balance()      # Masks balance behind ₦ ● ● ● ● ●
│   ├── _start_autohide()    # Recursive 1-second countdown to auto-mask
│   ├── _deposit()           # Adds funds, updates balance, logs history row
│   ├── _withdraw()          # Deducts funds (with insufficient-funds check)
│   ├── _check_balance()     # Triggers balance reveal + logs enquiry
│   ├── _add_history()       # Appends a colour-coded row to the history frame
│   ├── _tick()              # Updates live clock every second
│   └── _logout()            # Confirms and returns to PIN screen
│
└── class ATMApp             # Root window — manages screen transitions
    ├── _show_pin()          # Destroys current screen, mounts PINScreen
    └── _show_dashboard()    # Destroys current screen, mounts DashboardScreen

Design Decisions

- **Screen-swap pattern** — each screen is a `CTkFrame` that is `.pack()`'d and `.destroy()`'d on transition. No hidden frames or tab logic — only the active screen exists in memory.
- **Callback injection** — `PINScreen` receives `on_success` and `DashboardScreen` receives `on_logout` as constructor arguments. Neither screen knows about the other — all routing lives in `ATMApp`.
- **Recursive autohide** — balance auto-hide uses a recursive `master.after(1000, ...)` call rather than a background thread, keeping all UI updates on the main thread and avoiding tkinter thread-safety issues.
- **Flash utility** — the `flash()` helper uses a recursive `widget.after()` to toggle between two colours `n` times without blocking the event loop.


📁 Project Structure

python-bank-atm/
│
├── atm.py                   # ← Main application (single file)
├── requirements.txt         # Python dependencies
├── .gitignore               # Git exclusions
├── LICENSE                  # MIT License
├── CONTRIBUTING.md          # Contribution guidelines
└── README.md                # This file

⚙️ Configuration

All configurable constants are at the top of `atm.py`:

```python
CORRECT_PIN      = "1234"          # Change to your desired PIN
INITIAL_BALANCE  = 50_000_000.00   # Starting account balance
BANK_NAME        = "Micro-Finance BANK"

# Colours
ACCENT   = "#00D4FF"   # Cyan-blue — headers, labels, balance revealed
SUCCESS  = "#00E676"   # Green — successful transactions
DANGER   = "#FF5252"   # Red — errors and warnings
GOLD     = "#FFD700"   # Gold — balance amount display
BG_DARK  = "#0A0E1A"   # Deep navy — window background
CARD_BG  = "#0F1629"   # Slightly lighter — card panels
BORDER   = "#1E2D4A"   # Subtle border colour
TEXT_DIM = "#5A7A9A"   # Muted — secondary labels

🗺️ Roadmap

- [ ] **Database persistence** — SQLite to save balance and history across sessions
- [ ] **Multi-user support** — account number login alongside PIN
- [ ] **PIN hashing** — SHA-256 / bcrypt instead of plain string comparison
- [ ] **Lockout after 3 fails** — permanent lockout stored in DB
- [ ] **Session timeout** — auto-logout after N seconds of inactivity
- [ ] **Fund transfer** — send money to other accounts
- [ ] **Daily withdrawal limit** — configurable cap enforced via DB
- [ ] **CSV export** — download full transaction statement
- [ ] **Analytics tab** — pie chart (credits vs debits), balance trend graph
- [ ] **PyInstaller packaging** — standalone .exe / .app with no Python required


🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

1. Fork the repo
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "Add: your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

📜 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.


<div align="center">

Built with ❤️ and Python 🐍 in Lagos, Nigeria

⭐ **Star this repo if you found it useful!** ⭐

</div># python-bank-atm
