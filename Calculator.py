import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("简易计算器")

        # 创建显示框
        self.display = tk.Entry(master, width=30, justify="right")
        self.display.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        # 创建按钮
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
            tk.Button(master, text=button, command=cmd, width=5, height=2).grid(row=row, column=col, sticky="nsew")
            col += 1
            if col > 4:
                col = 0
                row += 1

        # 设置行列的权重，使得按钮可以自适应窗口大小
        for i in range(5):
            master.grid_columnconfigure(i, weight=1)
        for i in range(5):
            master.grid_rowconfigure(i, weight=1)

    def click(self, key):
        if key == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif key == '清除':
            self.display.delete(0, tk.END)
        elif key == '退位':
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, current[:-1])
        else:
            self.display.insert(tk.END, key)

root = tk.Tk()
calculator = Calculator(root)
root.mainloop()