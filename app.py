import tkinter as tk
from tkinter import messagebox
import pyperclip

from logic import generate_password, validate_length, check_password_strength

# ── Colour palette ──────────────────────────────────────────────────────────
BG        = "#1e1e2e"
SURFACE   = "#2a2a3e"
ACCENT    = "#7c6af7"
ACCENT2   = "#a78bfa"
TEXT      = "#e2e0f0"
SUBTEXT   = "#8884aa"
SUCCESS   = "#4ade80"
WARN      = "#facc15"
DANGER    = "#f87171"
ENTRY_BG  = "#13131f"

STRENGTH_COLORS = {
    "Weak":       DANGER,
    "Fair":       WARN,
    "Strong":     "#60a5fa",
    "Very Strong": SUCCESS,
}


def build_ui(root: tk.Tk) -> None:
    root.title("Password Generator")
    root.configure(bg=BG)
    root.resizable(False, False)

    # ── Title ────────────────────────────────────────────────────────────────
    tk.Label(
        root, text="🔐  Password Generator",
        bg=BG, fg=TEXT,
        font=("Courier New", 18, "bold"),
    ).pack(pady=(22, 4))

    tk.Label(
        root, text="Secure. Fast. Customisable.",
        bg=BG, fg=SUBTEXT,
        font=("Courier New", 9),
    ).pack(pady=(0, 16))

    # ── Length ───────────────────────────────────────────────────────────────
    frame_len = tk.Frame(root, bg=BG)
    frame_len.pack(fill="x", padx=30, pady=4)

    tk.Label(frame_len, text="Length", bg=BG, fg=TEXT,
             font=("Courier New", 10)).pack(side="left")

    length_var = tk.StringVar(value="16")
    length_entry = tk.Entry(
        frame_len, textvariable=length_var,
        width=5, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
        relief="flat", font=("Courier New", 11),
        highlightthickness=1, highlightbackground=ACCENT,
    )
    length_entry.pack(side="right")

    # ── Slider ───────────────────────────────────────────────────────────────
    slider_var = tk.IntVar(value=16)

    def on_slider(val):
        length_var.set(val)

    def on_entry_change(*_):
        try:
            v = int(length_var.get())
            if 4 <= v <= 128:
                slider_var.set(v)
        except ValueError:
            pass

    length_var.trace_add("write", on_entry_change)

    slider = tk.Scale(
        root, from_=4, to=128, orient="horizontal",
        variable=slider_var, command=on_slider,
        bg=BG, fg=SUBTEXT, troughcolor=SURFACE,
        highlightthickness=0, activebackground=ACCENT2,
        font=("Courier New", 8),
    )
    slider.pack(fill="x", padx=30)

    # ── Checkboxes ───────────────────────────────────────────────────────────
    use_numbers = tk.BooleanVar(value=True)
    use_symbols = tk.BooleanVar(value=True)

    def styled_check(parent, text, variable):
        cb = tk.Checkbutton(
            parent, text=text, variable=variable,
            bg=BG, fg=TEXT, selectcolor=SURFACE,
            activebackground=BG, activeforeground=ACCENT2,
            font=("Courier New", 10),
        )
        cb.pack(side="left", padx=10)

    frame_opts = tk.Frame(root, bg=BG)
    frame_opts.pack(pady=8)
    styled_check(frame_opts, "Include Numbers",  use_numbers)
    styled_check(frame_opts, "Include Symbols",  use_symbols)

    # ── Result display ───────────────────────────────────────────────────────
    result_var = tk.StringVar(value="")
    result_entry = tk.Entry(
        root, textvariable=result_var,
        width=36, bg=ENTRY_BG, fg=ACCENT2, insertbackground=ACCENT2,
        relief="flat", font=("Courier New", 12, "bold"),
        highlightthickness=1, highlightbackground=SURFACE,
        justify="center", state="readonly",
    )
    result_entry.pack(padx=30, pady=(12, 4))

    # ── Strength bar ─────────────────────────────────────────────────────────
    strength_label = tk.Label(
        root, text="", bg=BG, fg=SUBTEXT,
        font=("Courier New", 9, "italic"),
    )
    strength_label.pack()

    strength_canvas = tk.Canvas(root, bg=BG, height=6, width=280,
                                highlightthickness=0)
    strength_canvas.pack(pady=(2, 10))

    def update_strength_bar(password):
        label = check_password_strength(password)
        color = STRENGTH_COLORS.get(label, SUBTEXT)
        strength_label.config(text=f"Strength: {label}", fg=color)

        strength_canvas.delete("all")
        levels = ["Weak", "Fair", "Strong", "Very Strong"]
        idx = levels.index(label) + 1          # 1-4
        fill_w = int(280 * idx / 4)
        strength_canvas.create_rectangle(0, 0, 280, 6, fill=SURFACE, outline="")
        strength_canvas.create_rectangle(0, 0, fill_w, 6, fill=color, outline="")

    # ── Generate ─────────────────────────────────────────────────────────────
    def on_generate():
        try:
            length = validate_length(length_var.get())
        except ValueError as e:
            messagebox.showerror("Invalid Length", str(e))
            return

        password = generate_password(
            length,
            use_numbers=use_numbers.get(),
            use_symbols=use_symbols.get(),
        )
        result_var.set(password)
        update_strength_bar(password)

    # ── Copy ─────────────────────────────────────────────────────────────────
    copy_label = tk.Label(root, text="", bg=BG, fg=SUCCESS,
                          font=("Courier New", 9))
    copy_label.pack()

    def on_copy():
        pwd = result_var.get()
        if not pwd:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return
        try:
            pyperclip.copy(pwd)
            copy_label.config(text="✓ Copied to clipboard!")
            root.after(2000, lambda: copy_label.config(text=""))
        except Exception:
            messagebox.showinfo("Copy", f"Your password:\n{pwd}")

    # ── Buttons ──────────────────────────────────────────────────────────────
    frame_btns = tk.Frame(root, bg=BG)
    frame_btns.pack(pady=(4, 20))

    def btn(parent, text, cmd, color=ACCENT):
        b = tk.Button(
            parent, text=text, command=cmd,
            bg=color, fg="#ffffff", relief="flat",
            font=("Courier New", 10, "bold"),
            padx=14, pady=6, cursor="hand2",
            activebackground=ACCENT2, activeforeground="#ffffff",
        )
        b.pack(side="left", padx=6)

    btn(frame_btns, "⚡  Generate", on_generate)
    btn(frame_btns, "📋  Copy",     on_copy,     SURFACE)


def main():
    root = tk.Tk()
    build_ui(root)
    root.mainloop()


if __name__ == "__main__":
    main()