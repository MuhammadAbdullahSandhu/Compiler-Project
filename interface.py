import tkinter as tk
from tkinter import scrolledtext
import subprocess

class TerminalApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Python Terminal Interface")
        self.geometry("1200x1000")

        # Create a label for the command input field
        self.command_label = tk.Label(self, text="Enter Command:")
        self.command_label.pack(pady=5)

        # Create an entry box for command input
        self.command_entry = tk.Entry(self, width=100)
        self.command_entry.pack(pady=5)

        # Create a button to execute the command
        self.run_button = tk.Button(self, text="Run Command", command=self.run_command)
        self.run_button.pack(pady=5)

        # Create a scrolled text widget to show terminal output
        self.output_text = scrolledtext.ScrolledText(self, height=40, width=100)
        self.output_text.pack(pady=10)

        # Bind the Enter key to run the command
        self.command_entry.bind('<Return>', lambda event: self.run_command())

    def run_command(self):
        """Runs the command entered by the user and displays the output."""
        # Get the command from the entry box
        command = self.command_entry.get()

        # Clear the input field
        self.command_entry.delete(0, tk.END)

        if command.strip():  # Only run if the command is not empty
            try:
                # Run the command using subprocess and capture the output
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()

                # Clear the previous output
                self.output_text.delete(1.0, tk.END)

                # Display the command output or error
                if output:
                    self.output_text.insert(tk.END, output.decode("utf-8"))
                if error:
                    self.output_text.insert(tk.END, error.decode("utf-8"))

            except Exception as e:
                self.output_text.insert(tk.END, f"Error running command: {e}\n")

if __name__ == "__main__":
    app = TerminalApp()
    app.mainloop()
