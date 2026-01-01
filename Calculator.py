import tkinter as tk
from tkinter import messagebox, scrolledtext
import math

class CatCalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Neko Calculator")
        # Ukuran jendela 
        master.geometry("400x800") 
        master.resizable(False, False)

        # Variabel State
        self.current_theme = "Dark"
        self.expression = ""
        self.input_text = tk.StringVar()
        self.result_text = tk.StringVar(value="0")
        self.new_input_required = False
        self.max_history = 10

        self.themes = {
            "Dark": {
                "BG_WINDOW": '#1e1e2e',
                "DISPLAY_BG": '#1e1e2e',
                "FG_TEXT": '#cdd6f4',
                "FG_EXP": '#9399b2',
                "BTN_NUM": '#313244',
                "BTN_OP": '#fab387',
                "BTN_C": '#f38ba8',
                "BTN_EQ": '#a6e3a1',
                "BTN_SCI": '#45475a',
                "SCI_TEXT": '#cdd6f4',
                "HISTORY_BG": '#181825'
            },
            "Light": {
                "BG_WINDOW": '#eff1f5',
                "DISPLAY_BG": '#eff1f5',
                "FG_TEXT": '#4c4f69',
                "FG_EXP": '#8c8fa1',
                "BTN_NUM": '#e6e9ef',
                "BTN_OP": '#fe640b',
                "BTN_C": '#d20f39',
                "BTN_EQ": '#40a02b',
                "BTN_SCI": '#ccd0da',
                "SCI_TEXT": '#4c4f69',
                "HISTORY_BG": '#dce0e8'
            }
        }

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, fill='both')

        self.setup_ui()
        self.apply_theme()
        self.master.bind('<Key>', self.handle_keyboard)

    def setup_ui(self):
        # 1. Header (Theme & Actions)
        self.header_frame = tk.Frame(self.main_frame)
        self.header_frame.pack(fill='x', padx=20, pady=(15, 5))
        
        self.theme_btn = tk.Button(self.header_frame, text="🌙", command=self.toggle_theme, 
                                  font=('Arial', 10), bd=0, width=4, cursor="hand2")
        self.theme_btn.pack(side='left')

        self.save_btn = tk.Button(self.header_frame, text="Save", command=self.save_history_to_file,
                                 font=('Arial', 9, 'bold'), bd=0, padx=10, cursor="hand2")
        self.save_btn.pack(side='right', padx=(5, 0))

        self.copy_btn = tk.Button(self.header_frame, text="Copy", command=self.copy_to_clipboard,
                                 font=('Arial', 9, 'bold'), bd=0, padx=10, cursor="hand2")
        self.copy_btn.pack(side='right')

        # 2. Display Area
        self.display_frame = tk.Frame(self.main_frame)
        self.display_frame.pack(fill='x', padx=25, pady=(10, 10))

        self.expression_label = tk.Label(self.display_frame, textvariable=self.input_text, 
                                        font=('Segoe UI', 12), anchor='e')
        self.expression_label.pack(fill='x')

        self.result_label = tk.Label(self.display_frame, textvariable=self.result_text, 
                                    font=('Segoe UI', 48, 'bold'), anchor='e')
        self.result_label.pack(fill='x')

        # 3. Button Grid 
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill='both', padx=20, pady=10)

        for i in range(4): 
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(6): 
            self.button_frame.grid_rowconfigure(i, weight=1)
            
        self.create_buttons()

        # 4. History 
        self.history_frame = tk.Frame(self.main_frame)
        self.history_frame.pack(fill='both', padx=20, pady=(10, 20), expand=True)
        
        tk.Label(self.history_frame, text="RECENT HISTORY", font=('Arial', 8, 'bold'), 
                 bg=self.themes[self.current_theme]["BG_WINDOW"], 
                 fg=self.themes[self.current_theme]["FG_EXP"]).pack(anchor='w', pady=(0, 5))
        
        self.history_display = scrolledtext.ScrolledText(self.history_frame, height=6, 
                                                        font=('Consolas', 11), bd=0, 
                                                        padx=10, pady=10)
        self.history_display.pack(fill='both', expand=True)
        self.history_display.config(state='disabled')

    def create_buttons(self):
        colors = self.themes[self.current_theme]
        # Layout 4 kolom
        btns = [
            ('sin', 0, 0, colors["BTN_SCI"]), ('cos', 0, 1, colors["BTN_SCI"]), ('√', 0, 2, colors["BTN_SCI"]), ('/', 0, 3, colors["BTN_OP"]),
            ('C', 1, 0, colors["BTN_C"]), ('(', 1, 1, colors["BTN_OP"]), (')', 1, 2, colors["BTN_OP"]), ('←', 1, 3, colors["BTN_OP"]),
            ('7', 2, 0, colors["BTN_NUM"]), ('8', 2, 1, colors["BTN_NUM"]), ('9', 2, 2, colors["BTN_NUM"]), ('*', 2, 3, colors["BTN_OP"]),
            ('4', 3, 0, colors["BTN_NUM"]), ('5', 3, 1, colors["BTN_NUM"]), ('6', 3, 2, colors["BTN_NUM"]), ('-', 3, 3, colors["BTN_OP"]),
            ('1', 4, 0, colors["BTN_NUM"]), ('2', 4, 1, colors["BTN_NUM"]), ('3', 4, 2, colors["BTN_NUM"]), ('+', 4, 3, colors["BTN_OP"]),
            ('0', 5, 0, colors["BTN_NUM"], 2), ('.', 5, 2, colors["BTN_NUM"]), ('=', 5, 3, colors["BTN_EQ"])
        ]

        for b in btns:
            text, r, c, bg = b[0], b[1], b[2], b[3]
            span = b[4] if len(b) > 4 else 1
            
            fg_color = "#2d3436" if bg in [colors["BTN_OP"], colors["BTN_EQ"]] else colors["FG_TEXT"]
            if bg == colors["BTN_SCI"]: fg_color = colors["SCI_TEXT"]

            btn = tk.Button(self.button_frame, text=text, font=('Segoe UI', 16, 'bold'),
                           bg=bg, fg=fg_color, bd=0, relief='flat', 
                           cursor="hand2", activebackground=bg,
                           # Tinggi 
                           height=1, width=4, 
                           command=lambda t=text: self.button_click(t))
            btn.grid(row=r, column=c, columnspan=span, sticky="nsew", padx=3, pady=3)

    def apply_theme(self):
        colors = self.themes[self.current_theme]
        self.master.configure(bg=colors["BG_WINDOW"])
        self.main_frame.configure(bg=colors["BG_WINDOW"])
        self.header_frame.configure(bg=colors["BG_WINDOW"])
        self.history_frame.configure(bg=colors["BG_WINDOW"])
        
        self.expression_label.configure(bg=colors["DISPLAY_BG"], fg=colors["FG_EXP"])
        self.result_label.configure(bg=colors["DISPLAY_BG"], fg=colors["FG_TEXT"])
        
        self.history_display.config(state='normal')
        self.history_display.configure(bg=colors["HISTORY_BG"], fg=colors["FG_TEXT"])
        self.history_display.config(state='disabled')
        
        self.copy_btn.configure(bg=colors["BTN_SCI"], fg=colors["SCI_TEXT"])
        self.save_btn.configure(bg=colors["BTN_SCI"], fg=colors["SCI_TEXT"])
        self.theme_btn.config(bg=colors["BTN_NUM"], fg=colors["FG_TEXT"], 
                             text="☀️" if self.current_theme == "Dark" else "🌙")
        self.create_buttons()

    def button_click(self, text):
        if text == 'C':
            self.expression = ""
            self.input_text.set("")
            self.result_text.set("0")
        elif text == '←':
            self.expression = self.expression[:-1]
        elif text == '=':
            self.calculate_result()
            return
        else:
            if self.new_input_required and text.isdigit():
                self.expression = text
            else:
                mapping = {'sin': 'sin(', 'cos': 'cos(', '√': 'sqrt('}
                self.expression += mapping.get(text, str(text))
            self.new_input_required = False
        self.result_text.set(self.expression if self.expression else "0")

    def calculate_result(self):
        try:
            safe_dict = {"sin": lambda x: math.sin(math.radians(float(x))),
                         "cos": lambda x: math.cos(math.radians(float(x))),
                         "sqrt": lambda x: math.sqrt(float(x))}
            
            clean_expr = self.expression.replace('x', '*')
            res = eval(clean_expr, {"__builtins__": None}, safe_dict)
            
            if isinstance(res, float) and res.is_integer(): res = int(res)
            elif isinstance(res, float): res = round(res, 6)
            
            self.history_display.config(state='normal')
            self.history_display.insert('1.0', f" {self.expression} = {res}\n")
            self.history_display.config(state='disabled')
            
            self.input_text.set(self.expression + " =")
            self.result_text.set(res)
            self.expression = str(res)
            self.new_input_required = True
        except:
            self.result_label.config(fg='#f38ba8')
            self.master.after(200, lambda: self.result_label.config(fg=self.themes[self.current_theme]["FG_TEXT"]))
            messagebox.showerror("Error", "Input tidak valid")

    def toggle_theme(self):
        self.current_theme = "Light" if self.current_theme == "Dark" else "Dark"
        self.apply_theme()

    def copy_to_clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.result_text.get())
        messagebox.showinfo("Copy", "Hasil disalin!")

    def save_history_to_file(self):
        content = self.history_display.get("1.0", tk.END).strip()
        if not content: return
        with open("history.txt", "w") as f: f.write(content)
        messagebox.showinfo("Save", "Riwayat disimpan!")

    def handle_keyboard(self, event):
        if event.char.isdigit() or event.char in '+-*/.()': self.button_click(event.char)
        elif event.keysym == "Return": self.calculate_result()
        elif event.keysym == "BackSpace": self.button_click('←')
        elif event.keysym == "Escape": self.button_click('C')

if __name__ == "__main__":
    root = tk.Tk()
    app = CatCalculatorApp(root)
    root.mainloop()