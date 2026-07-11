"""
Modern Calculator App
----------------------
A polished, iOS-style GUI calculator built with Tkinter (Python standard library).
Run with: python calculator.py
"""

import tkinter as tk

# ---- Color palette ----
BG = "#0d0d0d"
DISPLAY_BG = "#0d0d0d"
PREVIEW_FG = "#8a8a8a"
RESULT_FG = "#ffffff"

NUM_BG = "#2b2b2b"
NUM_BG_HOVER = "#3d3d3d"
NUM_FG = "#ffffff"

FUNC_BG = "#a5a5a5"       # C, +/-, %
FUNC_BG_HOVER = "#c4c4c4"
FUNC_FG = "#0d0d0d"

OP_BG = "#ff9f0a"         # ÷ × − +
OP_BG_HOVER = "#ffb340"
OP_FG = "#ffffff"

EQ_BG = "#ff9f0a"
EQ_BG_HOVER = "#ffb340"


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.expression = ""
        self.input_text = tk.StringVar(value="0")
        self.preview_text = tk.StringVar(value="")

        self._build_display()
        self._build_buttons()

        self.bind("<Key>", self._on_key)

    # ---------------- UI construction ----------------

    def _build_display(self):
        display_frame = tk.Frame(self, bg=DISPLAY_BG)
        display_frame.pack(fill="both")

        preview = tk.Label(
            display_frame,
            textvariable=self.preview_text,
            font=("Segoe UI", 14),
            bg=DISPLAY_BG,
            fg=PREVIEW_FG,
            anchor="e",
            justify="right",
        )
        preview.pack(fill="x", padx=20, pady=(24, 0))

        result = tk.Label(
            display_frame,
            textvariable=self.input_text,
            font=("Segoe UI", 42),
            bg=DISPLAY_BG,
            fg=RESULT_FG,
            anchor="e",
            justify="right",
        )
        result.pack(fill="x", padx=20, pady=(0, 20))

    def _build_buttons(self):
        buttons_frame = tk.Frame(self, bg=BG)
        buttons_frame.pack(padx=16, pady=(0, 20))

        layout = [
            [("C", "func"), ("+/-", "func"), ("%", "func"), ("/", "op")],
            [("7", "num"), ("8", "num"), ("9", "num"), ("*", "op")],
            [("4", "num"), ("5", "num"), ("6", "num"), ("-", "op")],
            [("1", "num"), ("2", "num"), ("3", "num"), ("+", "op")],
            [("0", "num_wide"), (".", "num"), ("=", "eq")],
        ]

        for r, row_values in enumerate(layout):
            col = 0
            for value, kind in row_values:
                span = 2 if kind == "num_wide" else 1
                btn = self._make_button(buttons_frame, value, kind)
                btn.grid(
                    row=r, column=col, columnspan=span,
                    padx=6, pady=6,
                    sticky="nsew",
                )
                col += span

        for c in range(4):
            buttons_frame.grid_columnconfigure(c, minsize=70)

    def _make_button(self, parent, value, kind):
        colors = {
            "num": (NUM_BG, NUM_BG_HOVER, NUM_FG),
            "num_wide": (NUM_BG, NUM_BG_HOVER, NUM_FG),
            "func": (FUNC_BG, FUNC_BG_HOVER, FUNC_FG),
            "op": (OP_BG, OP_BG_HOVER, OP_FG),
            "eq": (EQ_BG, EQ_BG_HOVER, OP_FG),
        }
        bg, hover_bg, fg = colors[kind]

        btn = tk.Button(
            parent,
            text=value,
            font=("Segoe UI", 18, "bold" if kind in ("op", "eq", "func") else "normal"),
            width=6 if kind != "num_wide" else 13,
            height=2,
            bd=0,
            relief="flat",
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            cursor="hand2",
            command=lambda v=value: self._on_button(v),
        )
        btn.bind("<Enter>", lambda e, b=btn, c=hover_bg: b.configure(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg: b.configure(bg=c))
        return btn

    # ---------------- Logic ----------------

    def _on_button(self, value):
        if value == "C":
            self.expression = ""
        elif value == "+/-":
            self._toggle_sign()
        elif value == "=":
            self._evaluate()
            return
        else:
            self.expression += value

        self._refresh_display()

    def _toggle_sign(self):
        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        elif self.expression:
            self.expression = "-" + self.expression

    def _refresh_display(self):
        self.preview_text.set(self.expression)
        self.input_text.set(self.expression if self.expression else "0")

    def _evaluate(self):
        try:
            allowed = set("0123456789+-*/.%() ")
            if not self.expression or not set(self.expression) <= allowed:
                raise ValueError("Invalid expression")

            self.preview_text.set(self.expression)
            result = eval(self.expression, {"__builtins__": {}})
            self.input_text.set(str(result))
            self.expression = str(result)
        except Exception:
            self.input_text.set("Error")
            self.preview_text.set("")
            self.expression = ""

    def _on_key(self, event):
        char = event.char
        if char in "0123456789+-*/.%()":
            self.expression += char
            self._refresh_display()
        elif event.keysym == "Return":
            self._evaluate()
        elif event.keysym == "BackSpace":
            self.expression = self.expression[:-1]
            self._refresh_display()
        elif event.keysym == "Escape":
            self.expression = ""
            self._refresh_display()
            self.preview_text.set("")


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()