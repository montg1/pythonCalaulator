import tkinter as tk

lst_history = []

#set color for text and buttons
DARK_GRAY_SOFTER = "#2a2a2a"
DARK_GRAY = "#151515"
EQUAL_COLOR = "#fe036a"
LIGHT_GRAY = "#4a4a4a"
LABEL_COLOR = "white"

#font = "Eletrolize"
LARGE_FONT_STYLE = ("Eletrolize", 40, "bold")
SMALL_FONT_STYLE = ("Eletrolize", 16)
DIGITS_FONT_STYLE = ("Eletrolize", 24, "bold")
DEFAULT_FONT_STYLE = ("Eletrolize", 20)

class Calculator:



    def __init__(self):
        self.gui = tk.Tk()
        self.gui.geometry("900x900") #set gui size
        self.gui.title("Calculator") #set gui title

        self.total_expression = "" #set total expression
        self.current_expression = "" #set current expression
        self.display_frame = self.create_display_frame() #create display frame

        self.total_label, self.label = self.create_display_labels() #create display labels

        #create buttons frame
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        } 
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):#bind keys
        self.gui.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.gui.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.gui.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_history_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    

    def create_display_frame(self):
        frame = tk.Frame(self.gui, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=DARK_GRAY, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=DARK_GRAY_SOFTER, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=DARK_GRAY_SOFTER, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def is_prime_num(self):
        if int(self.current_expression) in (2,3,5,7):
            self.current_expression = str(f"{self.current_expression} is P")

        elif int(self.current_expression) % 2 != 0 and int(self.current_expression) % 3 != 0 and int(self.current_expression) % 5 != 0 and int(self.current_expression) % 7 != 0:
            self.current_expression = str(f"{self.current_expression} is P")
        else:
            self.current_expression = str(f"{self.current_expression} not P")
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="Is Prime Number?", bg=DARK_GRAY_SOFTER, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.is_prime_num)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=DARK_GRAY_SOFTER, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self): #evaluate expression
 
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            if self.total_expression != "":
                lst_history.append(f'{self.total_expression}') #add to history
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

            

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=EQUAL_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=1, sticky=tk.NSEW)

    def create_history_button(self):
        button = tk.Button(self.buttons_frame, text="H", bg=DARK_GRAY_SOFTER, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.show_history)
        button.grid(row=4, column=4, columnspan=1, sticky=tk.NSEW)

    def show_history(self):
        with open('history.txt', 'w') as file_history:
            for item in lst_history:
                file_history.write(f'{item}\n')
        history_window = tk.Toplevel(self.gui)
        history_window.title("History")
        history_window.geometry("500x500")
        history_window.configure(background=LIGHT_GRAY)
        history_window.resizable(False, False)
        history_window.focus_force()
        history_window.grab_set()
        with open("history.txt", "r+") as hir:#read history
            for line in hir:
                format_line = f"{line} = {eval(line)}"
                label = tk.Label(history_window, text=format_line, anchor=tk.E, bg=LIGHT_GRAY,
                                 fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
                label.pack(expand=True, fill='both')
          



    def create_buttons_frame(self):
        frame = tk.Frame(self.gui)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

        

    def update_label(self):
        self.label.config(text=self.current_expression[:11])
        


    def run(self):
        self.gui.mainloop()


if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()
