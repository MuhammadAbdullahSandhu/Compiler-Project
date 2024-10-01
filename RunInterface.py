import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from Lexer import Lexer
import MyParser

class TerminalApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Compiler Construction")
        self.configure(bg="#2e2e2e") 
        self.geometry(f"{1200}x{900}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        text_font = ("Consolas", 11)
        label_font = ("Arial", 12, "bold")
        self.command_label = tk.Label(self, text="Enter Source Code:", font=label_font, fg="#f0f0f0", bg="#2e2e2e")
        self.command_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.source_code_input = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD, font=text_font, bg="#3c3f41", fg="white", insertbackground="white")
        self.source_code_input.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.run_button = ttk.Button(self, text="Run Code", command=self.run_code_file, style="TButton")
        self.run_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.error_label = tk.Label(self, text="", font=label_font, fg="red", bg="#2e2e2e")
        self.error_label.grid(row=3, column=0, columnspan=2, pady=5)
        self.token_label = tk.Label(self, text="Tokens", font=label_font, fg="#f0f0f0", bg="#2e2e2e")
        self.token_label.grid(row=4, column=0, padx=10, pady=(5, 0), sticky='nw')

        self.parser_label = tk.Label(self, text="Parser Output", font=label_font, fg="#f0f0f0", bg="#2e2e2e")
        self.parser_label.grid(row=4, column=1, padx=10, pady=(5, 0), sticky='nw')

        self.ast_label = tk.Label(self, text="AST Output", font=label_font, fg="#f0f0f0", bg="#2e2e2e")
        self.ast_label.grid(row=5, column=0, padx=10, pady=(5, 0), sticky='nw')

        self.tac_label = tk.Label(self, text="TAC Output", font=label_font, fg="#f0f0f0", bg="#2e2e2e")
        self.tac_label.grid(row=5, column=1, padx=10, pady=(5, 0), sticky='nw')

        self.token_output = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD, font=text_font, bg="#3c3f41", fg="white", insertbackground="white")
        self.token_output.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')

        self.parser_output = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD, font=text_font, bg="#3c3f41", fg="white", insertbackground="white")
        self.parser_output.grid(row=4, column=1, padx=10, pady=10, sticky='nsew')

        self.ast_output = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD, font=text_font, bg="#3c3f41", fg="white", insertbackground="white")
        self.ast_output.grid(row=5, column=0, padx=10, pady=10, sticky='nsew')

        self.tac_output = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD, font=text_font, bg="#3c3f41", fg="white", insertbackground="white")
        self.tac_output.grid(row=5, column=1, padx=10, pady=10, sticky='nsew')

        # Customize button styles
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)

    def run_code_file(self):
        try:
            # Clear previous error messages
            self.error_label.config(text="")

            # Get source code from the text input area
            source_code = self.source_code_input.get(1.0, tk.END).strip()

            # If no input is provided, show an error
            if not source_code:
                self.error_label.config(text="Error: No source code provided.")
                return

            # Clear previous outputs
            self.token_output.delete(1.0, tk.END)
            self.parser_output.delete(1.0, tk.END)
            self.ast_output.delete(1.0, tk.END)
            self.tac_output.delete(1.0, tk.END)

            # Create tokens using the Lexer class
            tokens = Lexer(source_code)
            myparser = MyParser.Parser(tokens)

            # Display tokens in the token section
            self.token_output.insert(tk.END, "Tokens:\n")
            for token in tokens:
                self.token_output.insert(tk.END, f"{token}\n")

            # Run the parser and get the results
            try:
                # Unpack three values returned by parse()
                global_declarations, functions, program, st, tac_code = myparser.parse()
                # Display the parser result and AST
                self.parser_output.insert(tk.END, "Parsing completed successfully.\n")
                self.ast_output.insert(tk.END, f"AST: {functions}\n")

            except SyntaxError as e:
                self.error_label.config(text=f"Syntax error: {e}")

            try:
                # Display the parser result and AST
                self.parser_output.insert(tk.END, f"AST:\n{st}\n")
                self.tac_output.insert(tk.END, f"TAC:\n{tac_code}\n")

            except SyntaxError as e:
                self.error_label.config(text=f"Syntax error: {e}")

        except Exception as e:
            self.error_label.config(text=f"Error: {e}")


if __name__ == "__main__":
    app = TerminalApp()
    app.mainloop()
