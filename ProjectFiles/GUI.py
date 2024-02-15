
import tkinter as tk
from tkinter import messagebox, ttk
from logic import CommandManualGenerator, ManualVerifier, get_info_for_selection


class ManualViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Command Manual Viewer")

        self.commands = []  # Initialize commands list here
        self.selected_command = tk.StringVar()
        self.choice_var = tk.StringVar()

        # Create and configure widgets
        self.create_widgets()

    def create_widgets(self):
        # Generate manuals button
        generate_manuals_btn = tk.Button(self.master, text="Generate Manuals", command=self.generate_manuals)
        generate_manuals_btn.pack(pady=10)

        # Verify manuals button
        self.verify_manuals_btn = tk.Button(self.master, text="Verify Manuals", command=self.verify_manuals)
        self.verify_manuals_btn.pack(pady=10)

        # Dropdown list for commands (initially disabled)
        self.command_dropdown = ttk.Combobox(self.master, textvariable=self.selected_command, state="readonly")
        self.command_dropdown.pack(pady=10)
        # Set a default prompt for the dropdown list
        self.command_dropdown.set("Choose Command")

        # Manual display text box
        self.manual_display = tk.Text(self.master, wrap=tk.WORD, height=15, width=60, state=tk.DISABLED)
        self.manual_display.pack(pady=10)

        # Radio buttons for user choice (initially disabled)
        radio_frame = tk.Frame(self.master)
        radio_frame.pack(pady=10)

        choices = ["Show All Info", "Show Description", "Show Version", "Show Example",
                   "Show Related Commands", "Show Online Documentation Links", "Show Recommended Commands"]

        radio_frame = tk.Frame(self.master)
        radio_frame.pack()

        self.radio_buttons = []

        row_count = 0
        col_count = 0

        for choice in choices:
            radio_button = tk.Radiobutton(radio_frame, text=choice, variable=self.choice_var, value=choice,
                                          state=tk.DISABLED)
            radio_button.grid(row=row_count, column=col_count, sticky=tk.W)

            self.radio_buttons.append(radio_button)

            col_count += 1
            if col_count == 4:
                col_count = 0
                row_count += 1

        # Set a default value for the radio buttons
        self.choice_var.set("Show All Info")

        # Search button (initially disabled)
        self.search_btn = tk.Button(self.master, text="Search", command=self.display_manual_info, state=tk.DISABLED)
        self.search_btn.pack(pady=5)

    def generate_manuals(self):
        generator = CommandManualGenerator("input_commands.txt")
        c = generator.generate_manuals()

        if type(c) is str:
            self.show_message("ERROR", c, is_error=True)
        else:
            self.commands = c
            self.show_message("SUCCESS", "Manuals generated successfully.")

    def display_manual_info(self):
        selected_command = self.selected_command.get()
        user_choice = self.choice_var.get()

        if not selected_command or selected_command == "Choose Command":
            self.show_message("Attention", "Please select a valid command to display.")
            return

        info = get_info_for_selection(selected_command, user_choice)

        # Enable the Text widget for writing
        self.manual_display.config(state=tk.NORMAL)

        self.manual_display.delete(1.0, tk.END)
        self.manual_display.insert(tk.END, info)

        # Disable the Text widget to prevent user input
        self.manual_display.config(state=tk.DISABLED)

    def verify_manuals(self):

        generator = CommandManualGenerator("input_commands.txt")
        c = generator.read_commands_from_file()

        if type(c) is str:
            self.show_message("ERROR", c, is_error=True)
        else:
            self.commands = c

            verifier = ManualVerifier("manuals_folder", "input_commands.txt")
            verification_messages = verifier.verify_manuals(self.commands)

            success_message = []
            error_message = []

            for message in verification_messages:
                if message.endswith("successfully"):
                    success_message.append(message)
                else:
                    error_message.append(message)

            s_message = ""
            f_message = ""

            if len(success_message) != 0:
                for m in success_message:
                    s_message += m
                    s_message += "\n"
                self.show_message("Verification Success", s_message)

            if len(error_message) != 0:
                for m in error_message:
                    f_message += m
                    f_message += "\n"
                self.show_message("Verification Errors", f_message, is_error=True)
                self.disable_search_button()  # Disable the search button in case of verification errors
                self.show_message("Attention", "you should regenerate the manuals", is_error=True)

            if len(success_message) == len(self.commands):
                self.enable_search_button()  # Enable the search button

                self.command_dropdown.config(state="readonly")
                # Populate the dropdown list with generated commands
                self.command_dropdown['values'] = self.commands

    def enable_search_button(self):
        self.search_btn.config(state=tk.NORMAL)  # Enable the search button
        for radio_button in self.radio_buttons:
            radio_button.config(state=tk.NORMAL)  # Enable radio buttons

    def disable_search_button(self):
        self.search_btn.config(state=tk.DISABLED)  # Disable the search button
        for radio_button in self.radio_buttons:
            radio_button.config(state=tk.DISABLED)  # Disable radio buttons

    @staticmethod
    def show_message(title, message="", is_error=False):
        if not is_error:
            messagebox.showinfo(title, message)
        else:
            messagebox.showerror(title, message)

    def mainloop(self):
        self.master.mainloop()


def main():
    root = tk.Tk()
    app = ManualViewerApp(root)

    # Set the window size
    root.geometry("1000x600")  # Change the width and height as needed

    app.mainloop()


if __name__ == "__main__":
    main()
