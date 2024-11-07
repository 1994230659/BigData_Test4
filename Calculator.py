import tkinter as tk
import math
from tkinter import ttk


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("计算器")
        self.is_scientific = False
        self.history = []

        # 创建左右分隔的框架
        self.main_frame = ttk.PanedWindow(master, orient=tk.HORIZONTAL)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧计算器框架
        self.calculator_frame = ttk.Frame(self.main_frame)
        self.main_frame.add(self.calculator_frame)

        # 右侧历史记录框架
        self.history_frame = ttk.Frame(self.main_frame)
        self.main_frame.add(self.history_frame)

        # 创建显示框
        self.display = tk.Entry(self.calculator_frame, width=30, justify="right")
        self.display.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

        # 创建基本按钮
        self.create_buttons()

        # 创建切换按钮
        self.switch_button = tk.Button(self.calculator_frame, text="切换到科学型", command=self.toggle_scientific,
                                       width=10, height=2)
        self.switch_button.grid(row=5, column=0, columnspan=5, sticky="nsew")

        # 设置计算器框架的行列权重
        for i in range(6):
            self.calculator_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.calculator_frame.grid_rowconfigure(i, weight=1)

        # 创建历史记录显示
        self.history_display = tk.Text(self.history_frame, width=30, height=20)
        self.history_display.pack(fill=tk.BOTH, expand=True)
        self.history_display.config(state=tk.DISABLED)

        # 创建清除历史按钮
        self.clear_history_button = tk.Button(self.history_frame, text="清除历史", command=self.clear_history)
        self.clear_history_button.pack(fill=tk.X)

    def create_buttons(self):
        buttons = [
            '7', '8', '9', '/', '(',
            '4', '5', '6', '*', ')',
            '1', '2', '3', '-', '清除',
            '0', '.', '=', '+', '退位'
        ]

        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            tk.Button(self.calculator_frame, text=button, command=cmd, width=5, height=2).grid(row=row, column=col,
                                                                                               sticky="nsew")
            col += 1
            if col > 4:
                col = 0
                row += 1

    def create_scientific_buttons(self):
        buttons = [
            'sin', 'cos', 'tan', 'log', '√',
            'π', 'e', '^', '(', ')',
            '7', '8', '9', '/', '清除',
            '4', '5', '6', '*', '退位',
            '1', '2', '3', '-', 'Ans',
            '0', '.', '=', '+', 'Mod'
        ]

        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            tk.Button(self.calculator_frame, text=button, command=cmd, width=5, height=2).grid(row=row, column=col,
                                                                                               sticky="nsew")
            col += 1
            if col > 4:
                col = 0
                row += 1

    def toggle_scientific(self):
        self.is_scientific = not self.is_scientific
        for widget in self.calculator_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget != self.switch_button:
                widget.destroy()

        if self.is_scientific:
            self.create_scientific_buttons()
            self.switch_button.config(text="切换到基本型")
        else:
            self.create_buttons()
            self.switch_button.config(text="切换到科学型")

    def click(self, key):
        if key == '=':
            try:
                expression = self.display.get()
                result = self.evaluate(expression)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.add_to_history(f"{expression} = {result}")
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.add_to_history("Error")
        elif key == '清除':
            self.display.delete(0, tk.END)
        elif key == '退位':
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, current[:-1])
        elif key in ['sin', 'cos', 'tan', 'log', '√']:
            self.display.insert(tk.END, key + '(')
        elif key == 'π':
            self.display.insert(tk.END, 'π')
        elif key == 'e':
            self.display.insert(tk.END, 'e')
        elif key == '^':
            self.display.insert(tk.END, '**')
        elif key == 'Mod':
            self.display.insert(tk.END, '%')
        else:
            self.display.insert(tk.END, key)

    def evaluate(self, expression):
        expression = expression.replace('π', str(math.pi))
        expression = expression.replace('e', str(math.e))
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('log', 'math.log10')
        expression = expression.replace('√', 'math.sqrt')
        return eval(expression)

    def add_to_history(self, entry):
        self.history.append(entry)
        self.history_display.config(state=tk.NORMAL)
        self.history_display.insert(tk.END, entry + "\n")
        self.history_display.see(tk.END)
        self.history_display.config(state=tk.DISABLED)

    def clear_history(self):
        self.history = []
        self.history_display.config(state=tk.NORMAL)
        self.history_display.delete('1.0', tk.END)
        self.history_display.config(state=tk.DISABLED)


root = tk.Tk()
calculator = Calculator(root)
root.mainloop()