import tkinter as tk
from tkinter import font


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("電卓")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        self.expression = ""

        display_font = font.Font(family="Segoe UI", size=24)
        btn_font = font.Font(family="Segoe UI", size=14)

        self.display_var = tk.StringVar(value="0")
        display = tk.Label(
            root,
            textvariable=self.display_var,
            font=display_font,
            bg="#0f0f1a",
            fg="white",
            anchor="e",
            padx=15,
            pady=20,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        buttons = [
            ("C", 1, 0, "clear"), ("←", 1, 1, "clear"), ("%", 1, 2, "op"), ("÷", 1, 3, "op"),
            ("7", 2, 0, "num"), ("8", 2, 1, "num"), ("9", 2, 2, "num"), ("×", 2, 3, "op"),
            ("4", 3, 0, "num"), ("5", 3, 1, "num"), ("6", 3, 2, "num"), ("−", 3, 3, "op"),
            ("1", 4, 0, "num"), ("2", 4, 1, "num"), ("3", 4, 2, "num"), ("+", 4, 3, "op"),
            ("0", 5, 0, "num"), (".", 5, 1, "num"), ("=", 5, 2, "eq"),
        ]

        colors = {
            "num": ("#313244", "white"),
            "op": ("#f38ba8", "#1e1e2e"),
            "eq": ("#a6e3a1", "#1e1e2e"),
            "clear": ("#f9e2af", "#1e1e2e"),
        }

        for text, r, c, kind in buttons:
            bg, fg = colors[kind]
            colspan = 2 if text == "=" else 1
            btn = tk.Button(
                root,
                text=text,
                font=btn_font,
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                bd=0,
                width=5,
                height=2,
                command=lambda t=text: self.on_click(t),
            )
            btn.grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=4, pady=4)

        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

        root.bind("<Key>", self.on_key)

    def on_click(self, t):
        if t == "C":
            self.expression = ""
        elif t == "←":
            self.expression = self.expression[:-1]
        elif t == "=":
            self.evaluate()
            return
        else:
            mapping = {"÷": "/", "×": "*", "−": "-"}
            self.expression += mapping.get(t, t)
        self.refresh()

    def on_key(self, event):
        k = event.keysym
        ch = event.char
        if ch and ch in "0123456789.+-*/%":
            self.expression += ch
            self.refresh()
        elif k in ("Return", "equal"):
            self.evaluate()
        elif k == "BackSpace":
            self.expression = self.expression[:-1]
            self.refresh()
        elif k == "Escape":
            self.expression = ""
            self.refresh()

    def evaluate(self):
        if not self.expression:
            return
        try:
            result = eval(self.expression, {"__builtins__": {}}, {})
            if isinstance(result, float):
                result = round(result, 10)
            self.expression = str(result)
        except Exception:
            self.expression = ""
            self.display_var.set("Error")
            return
        self.refresh()

    def refresh(self):
        shown = self.expression.replace("*", "×").replace("/", "÷").replace("-", "−")
        self.display_var.set(shown if shown else "0")


if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
