# ============================================================
#          BANK ATM — CustomTkinter GUI
# ============================================================

import customtkinter as ctk
from tkinter import messagebox
import time
import threading

# ─── App Theme ───────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─── Constants ───────────────────────────────────────────────
CORRECT_PIN = "1234"
INITIAL_BALANCE = 50000_000.00
BANK_NAME = "Micro-Finance BANK"
ACCENT   = "#00D4FF"      # cyan-blue accent
SUCCESS  = "#00E676"      # green
DANGER   = "#FF5252"      # red
GOLD     = "#FFD700"      # gold for balance
BG_DARK  = "#0A0E1A"      # deep navy background
CARD_BG  = "#0F1629"      # card panel
BORDER   = "#1E2D4A"      # subtle border
TEXT_DIM = "#5A7A9A"      # muted text

# ═══════════════════════════════════════════════════════════════
#  HELPER — animated label flash
# ═══════════════════════════════════════════════════════════════
def flash(widget, color, original, times=4, interval=180):
    """Flash a label colour to signal success / error."""
    def _flash(n):
        if n <= 0:
            widget.configure(text_color=original)
            return
        widget.configure(text_color=color if n % 2 == 0 else original)
        widget.after(interval, lambda: _flash(n - 1))
    _flash(times)

# ═══════════════════════════════════════════════════════════════
#  SCREEN  1 — PIN Entry
# ═══════════════════════════════════════════════════════════════
class PINScreen(ctk.CTkFrame):
    def __init__(self, master, on_success):
        super().__init__(master, fg_color="transparent")
        self.on_success = on_success
        self._build()

    def _build(self):
        # ── Bank logo / header ──────────────────────────────
        logo_frame = ctk.CTkFrame(self, fg_color=CARD_BG,
                                  corner_radius=20,
                                  border_width=1, border_color=BORDER)
        logo_frame.pack(fill="x", padx=40, pady=(40, 20))

        ctk.CTkLabel(logo_frame, text="🏦", font=("Helvetica", 52)
                     ).pack(pady=(24, 4))
        ctk.CTkLabel(logo_frame, text=BANK_NAME,
                     font=("Georgia", 28, "bold"), text_color=ACCENT
                     ).pack()
        ctk.CTkLabel(logo_frame, text="Automated Teller Machine",
                     font=("Helvetica", 12), text_color=TEXT_DIM
                     ).pack(pady=(2, 20))

        # ── PIN card ─────────────────────────────────────────
        card = ctk.CTkFrame(self, fg_color=CARD_BG,
                            corner_radius=20,
                            border_width=1, border_color=BORDER)
        card.pack(fill="x", padx=40, pady=10)

        ctk.CTkLabel(card, text="ENTER YOUR PIN",
                     font=("Helvetica", 13, "bold"), text_color=TEXT_DIM
                     ).pack(pady=(24, 6))

        # PIN display (masked dots)
        self._pin_var = ctk.StringVar()
        self._pin_display = ctk.CTkLabel(
            card, textvariable=self._pin_var,
            font=("Courier", 32, "bold"), text_color=ACCENT,
            width=200, height=50
        )
        self._pin_display.pack(pady=4)

        self._hint = ctk.CTkLabel(card, text=" ",
                                  font=("Helvetica", 12),
                                  text_color=DANGER)
        self._hint.pack(pady=(0, 6))

        # Numpad
        numpad = ctk.CTkFrame(card, fg_color="transparent")
        numpad.pack(padx=30, pady=(6, 24))
        self._pin_digits = []

        keys = [
            ["1","2","3"],
            ["4","5","6"],
            ["7","8","9"],
            ["⌫","0","✔"],
        ]
        btn_style = dict(width=72, height=52, corner_radius=10,
                         font=("Helvetica", 18, "bold"))
        for r, row in enumerate(keys):
            for c, k in enumerate(row):
                if k == "⌫":
                    fg, hover = "#1E2D4A", "#2A3D5A"
                elif k == "✔":
                    fg, hover = "#005C4B", "#007A63"
                else:
                    fg, hover = "#152238", "#1E3050"
                b = ctk.CTkButton(numpad, text=k,
                                  fg_color=fg, hover_color=hover,
                                  text_color="white",
                                  command=lambda x=k: self._key(x),
                                  **btn_style)
                b.grid(row=r, column=c, padx=5, pady=5)

        # Keyboard shortcut
        self.master.bind("<Key>", self._kb)

    # ── PIN helpers ─────────────────────────────────────────
    def _key(self, k):
        if k == "⌫":
            self._pin_digits = self._pin_digits[:-1]
        elif k == "✔":
            self._verify()
            return
        elif len(self._pin_digits) < 4:
            self._pin_digits.append(k)
        self._pin_var.set("●" * len(self._pin_digits))

    def _kb(self, event):
        if event.char.isdigit():
            self._key(event.char)
        elif event.keysym == "BackSpace":
            self._key("⌫")
        elif event.keysym == "Return":
            self._verify()

    def _verify(self):
        pin = "".join(self._pin_digits)
        if pin == CORRECT_PIN:
            self._hint.configure(text="✔  Access Granted", text_color=SUCCESS)
            self.master.after(700, self.on_success)
        else:
            self._pin_digits = []
            self._pin_var.set("")
            self._hint.configure(text="✖  Incorrect PIN. Try again.", text_color=DANGER)
            flash(self._hint, DANGER, DANGER, times=6)


# ═══════════════════════════════════════════════════════════════
#  SCREEN  2 — Main ATM Dashboard
# ═══════════════════════════════════════════════════════════════
class DashboardScreen(ctk.CTkFrame):
    def __init__(self, master, on_logout):
        super().__init__(master, fg_color="transparent")
        self.on_logout = on_logout
        self.balance = INITIAL_BALANCE
        self._build()

    def _build(self):
        # ── Top bar ─────────────────────────────────────────
        topbar = ctk.CTkFrame(self, fg_color=CARD_BG,
                              corner_radius=0, height=56,
                              border_width=1, border_color=BORDER)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        ctk.CTkLabel(topbar, text=f"🏦  {BANK_NAME}",
                     font=("Georgia", 18, "bold"), text_color=ACCENT
                     ).pack(side="left", padx=20, pady=12)

        self._time_lbl = ctk.CTkLabel(topbar, text="",
                                      font=("Courier", 12),
                                      text_color=TEXT_DIM)
        self._time_lbl.pack(side="right", padx=20)
        self._tick()

        ctk.CTkButton(topbar, text="⏻  Logout", width=100, height=32,
                      fg_color=DANGER, hover_color="#C62828",
                      font=("Helvetica", 12, "bold"),
                      command=self._logout
                      ).pack(side="right", padx=10)

        # ── Balance card ─────────────────────────────────────
        bal_card = ctk.CTkFrame(self, fg_color=CARD_BG,
                                corner_radius=20,
                                border_width=1, border_color=BORDER)
        bal_card.pack(fill="x", padx=30, pady=(20, 10))

        # Header row: label + eye toggle button
        bal_header = ctk.CTkFrame(bal_card, fg_color="transparent")
        bal_header.pack(fill="x", padx=20, pady=(20, 4))

        ctk.CTkLabel(bal_header, text="AVAILABLE BALANCE",
                     font=("Helvetica", 11, "bold"), text_color=TEXT_DIM
                     ).pack(side="left")

        self._bal_visible = False          # hidden by default
        self._autohide_job = None

        self._eye_btn = ctk.CTkButton(
            bal_header, text="👁  Show", width=80, height=26,
            font=("Helvetica", 11), corner_radius=12,
            fg_color="#1E2D4A", hover_color="#2A3D5A",
            command=self._toggle_balance
        )
        self._eye_btn.pack(side="right")

        # Balance display — hidden by default
        self._bal_lbl = ctk.CTkLabel(bal_card, text="₦ ● ● ● ● ●",
                                     font=("Georgia", 38, "bold"),
                                     text_color=TEXT_DIM)
        self._bal_lbl.pack()

        # Countdown label (shows "Hiding in 5s…")
        self._hide_countdown = ctk.CTkLabel(bal_card, text=" ",
                                            font=("Helvetica", 10),
                                            text_color=TEXT_DIM)
        self._hide_countdown.pack()

        ctk.CTkLabel(bal_card, text="Nigerian Naira (NGN)",
                     font=("Helvetica", 11), text_color=TEXT_DIM
                     ).pack(pady=(2, 20))

        # ── Status label (feedback messages) ─────────────────
        self._status = ctk.CTkLabel(self, text=" ",
                                    font=("Helvetica", 13),
                                    text_color=SUCCESS)
        self._status.pack(pady=(0, 4))

        # ── Transaction input area ────────────────────────────
        input_card = ctk.CTkFrame(self, fg_color=CARD_BG,
                                  corner_radius=20,
                                  border_width=1, border_color=BORDER)
        input_card.pack(fill="x", padx=30, pady=4)

        ctk.CTkLabel(input_card, text="TRANSACTION AMOUNT",
                     font=("Helvetica", 11, "bold"), text_color=TEXT_DIM
                     ).pack(pady=(16, 6))

        entry_row = ctk.CTkFrame(input_card, fg_color="transparent")
        entry_row.pack(padx=20)

        ctk.CTkLabel(entry_row, text="₦",
                     font=("Georgia", 22, "bold"), text_color=ACCENT
                     ).pack(side="left", padx=(0, 6))
        self._amount_var = ctk.StringVar()
        self._entry = ctk.CTkEntry(
            entry_row, textvariable=self._amount_var,
            placeholder_text="0.00",
            font=("Courier", 20), width=240, height=46,
            border_color=BORDER, fg_color="#0A1020",
            justify="right"
        )
        self._entry.pack(side="left")
        self._entry.bind("<Return>", lambda e: None)

        # Quick-amount chips
        chip_row = ctk.CTkFrame(input_card, fg_color="transparent")
        chip_row.pack(pady=(10, 16))
        for amt in [500, 1_000, 5_000, 10_000, 20_000, 50_000]:
            ctk.CTkButton(
                chip_row, text=f"₦{amt:,}", width=82, height=28,
                font=("Helvetica", 11),
                fg_color="#152238", hover_color="#1E3050",
                corner_radius=14,
                command=lambda a=amt: self._amount_var.set(str(float(a)))
            ).pack(side="left", padx=4)

        # ── Action buttons ────────────────────────────────────
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(pady=14)

        actions = [
            ("💰  Deposit",  "#00695C", "#00897B", self._deposit),
            ("🏧  Withdraw", "#1A237E", "#283593", self._withdraw),
            ("📋  Balance",  "#4A148C", "#6A1B9A", self._check_balance),
        ]
        for label, fg, hover, cmd in actions:
            ctk.CTkButton(
                btn_row, text=label, width=156, height=52,
                font=("Helvetica", 14, "bold"),
                fg_color=fg, hover_color=hover, corner_radius=14,
                command=cmd
            ).pack(side="left", padx=8)

        # ── Transaction history ───────────────────────────────
        hist_card = ctk.CTkFrame(self, fg_color=CARD_BG,
                                 corner_radius=20,
                                 border_width=1, border_color=BORDER)
        hist_card.pack(fill="both", expand=True, padx=30, pady=(4, 24))

        ctk.CTkLabel(hist_card, text="RECENT TRANSACTIONS",
                     font=("Helvetica", 11, "bold"), text_color=TEXT_DIM
                     ).pack(anchor="w", padx=16, pady=(14, 6))

        self._hist_box = ctk.CTkScrollableFrame(
            hist_card, fg_color="transparent", height=130)
        self._hist_box.pack(fill="both", expand=True, padx=10, pady=(0, 12))

        self._history = []
        self._add_history("System", "Session started", self.balance)

    # ── Helpers ──────────────────────────────────────────────
    def _fmt(self, v):
        return f"₦{v:,.2f}"

    def _tick(self):
        self._time_lbl.configure(
            text=time.strftime("  %a %d %b %Y   %H:%M:%S  "))
        self.master.after(1000, self._tick)

    # ── Balance visibility ───────────────────────────────────
    def _toggle_balance(self):
        if self._bal_visible:
            self._hide_balance()
        else:
            self._show_balance()

    def _show_balance(self):
        self._bal_visible = True
        self._bal_lbl.configure(text=self._fmt(self.balance), text_color=GOLD)
        self._eye_btn.configure(text="🙈  Hide")
        self._cancel_autohide()
        self._start_autohide(5)   # auto-hide after 5 seconds

    def _hide_balance(self):
        self._bal_visible = False
        self._bal_lbl.configure(text="₦ ● ● ● ● ●", text_color=TEXT_DIM)
        self._eye_btn.configure(text="👁  Show")
        self._hide_countdown.configure(text=" ")
        self._cancel_autohide()

    def _cancel_autohide(self):
        if self._autohide_job:
            self.master.after_cancel(self._autohide_job)
            self._autohide_job = None

    def _start_autohide(self, secs_left):
        if secs_left <= 0:
            self._hide_balance()
            return
        self._hide_countdown.configure(
            text=f"Hiding in {secs_left}s…", text_color=TEXT_DIM)
        self._autohide_job = self.master.after(
            1000, lambda: self._start_autohide(secs_left - 1))

    def _get_amount(self):
        try:
            val = float(self._amount_var.get())
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            self._set_status("⚠  Enter a valid positive amount.", DANGER)
            flash(self._status, DANGER, DANGER)
            return None

    def _set_status(self, msg, color=SUCCESS):
        self._status.configure(text=msg, text_color=color)

    def _update_balance(self):
        if self._bal_visible:
            self._bal_lbl.configure(text=self._fmt(self.balance), text_color=GOLD)
        else:
            self._bal_lbl.configure(text="₦ ● ● ● ● ●", text_color=TEXT_DIM)

    def _add_history(self, txn_type, detail, bal_after):
        ts = time.strftime("%H:%M:%S")
        color = SUCCESS if "Deposit" in txn_type or "System" in txn_type else (
                DANGER if "Withdraw" in txn_type else ACCENT)

        row = ctk.CTkFrame(self._hist_box, fg_color="#101828",
                           corner_radius=8)
        row.pack(fill="x", pady=3, padx=4)

        ctk.CTkLabel(row, text=f"[{ts}]",
                     font=("Courier", 10), text_color=TEXT_DIM,
                     width=70).pack(side="left", padx=(8, 4), pady=6)
        ctk.CTkLabel(row, text=txn_type,
                     font=("Helvetica", 11, "bold"), text_color=color,
                     width=90).pack(side="left")
        ctk.CTkLabel(row, text=detail,
                     font=("Helvetica", 11), text_color="white"
                     ).pack(side="left", padx=8)
        ctk.CTkLabel(row, text=f"Bal: {self._fmt(bal_after)}",
                     font=("Courier", 11), text_color=GOLD
                     ).pack(side="right", padx=12)

    # ── Actions ──────────────────────────────────────────────
    def _deposit(self):
        amt = self._get_amount()
        if amt is None:
            return
        self.balance += amt
        self._update_balance()
        self._set_status(f"✔  Deposit of {self._fmt(amt)} successful.", SUCCESS)
        self._add_history("Deposit", f"+{self._fmt(amt)}", self.balance)
        self._amount_var.set("")
        flash(self._bal_lbl, SUCCESS, GOLD)

    def _withdraw(self):
        amt = self._get_amount()
        if amt is None:
            return
        if amt > self.balance:
            self._set_status("✖  Insufficient funds. Transaction declined.", DANGER)
            flash(self._bal_lbl, DANGER, GOLD)
            return
        self.balance -= amt
        self._update_balance()
        self._set_status(f"✔  Withdrawal of {self._fmt(amt)} successful.", SUCCESS)
        self._add_history("Withdrawal", f"-{self._fmt(amt)}", self.balance)
        self._amount_var.set("")
        flash(self._bal_lbl, SUCCESS, GOLD)

    def _check_balance(self):
        self._set_status(f"ℹ  Your balance is {self._fmt(self.balance)}", ACCENT)
        self._add_history("Enquiry", "Balance checked", self.balance)
        self._show_balance()           # reveal + start 5-second countdown
        flash(self._bal_lbl, ACCENT, GOLD)

    def _logout(self):
        if messagebox.askyesno("Logout", "End this session?"):
            self.on_logout()


# ═══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════
class ATMApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Python Bank ATM")
        self.geometry("540x760")
        self.minsize(480, 700)
        self.resizable(True, True)
        self.configure(fg_color=BG_DARK)

        # Decorative accent bar across the top
        accent_bar = ctk.CTkFrame(self, height=4,
                                  fg_color=ACCENT, corner_radius=0)
        accent_bar.pack(fill="x", side="top")

        self._current_screen = None
        self._show_pin()

    def _clear(self):
        if self._current_screen:
            self._current_screen.destroy()

    def _show_pin(self):
        self._clear()
        self._current_screen = PINScreen(self, on_success=self._show_dashboard)
        self._current_screen.pack(fill="both", expand=True)

    def _show_dashboard(self):
        self._clear()
        self._current_screen = DashboardScreen(self, on_logout=self._show_pin)
        self._current_screen.pack(fill="both", expand=True)


# ─── Entry point ─────────────────────────────────────────────
if __name__ == "__main__":
    app = ATMApp()
    app.mainloop()