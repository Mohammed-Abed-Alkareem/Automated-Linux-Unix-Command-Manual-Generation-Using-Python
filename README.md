# Automated-Linux-Unix-Command-Manual-Generation-Using-Python
The project aims to automate the generation of a system manual for Linux/Unix commands using Python. The script developed will facilitate the creation of a Text file document structured as a template for each command.

# Code clarifying 
The project includes two main Python files: "GUI.py" and "logic.py". "GUI.py" creates the user interface, making it easy for users to view and interact with the application. "logic.py" handles the behind-the-scenes work, processing the data that the user sees. Together, these files make the application both user-friendly and efficient.
## "logic.py"
###	Class CommandManualGenerator:
This class is responsible for generating command manuals from a given input file. It reads and processes command names, preparing it for further use in the application.
#### •	init(self, input_file)
This method is the constructor for CommandManualGenerator class. It initializes a new instance of the class with a specific input file.
#### •	read_commands_from_file(self)
reads commands from a file and stores them in a list. It opens the input file, reads each line, removes extra spaces, and adds the lines to a list. If the file is not found, it returns an error message.
#### •	generate_manuals(self)
reads commands from a file, turns each command into a manual, and then converts these manuals into XML format.
### 	Class CommandManual
#### •	init(self, command)
Initializes the CommandManual instance with the specified command. It sets self.command to the provided command, which will be used in other methods to generate manual content.
#### •	generate_manual(self)
Compiles a complete manual for the command. This function calls other methods to get the command's description, version history, examples, related commands, online documentation links, and recommended commands, and then assembles this information into a dictionary representing the command manual.
#### •	get_command_description(self)
Tries to retrieve the description of the command. It first attempts to get the description from the man page. If unsuccessful, it tries the --help option of the command. The method handles errors and returns the command description or an error message if the description is not available.
#### •	get_version_history(self)
Attempts to fetch the version history of the command. This method tries several approaches: first the --version option, then -v, and finally looks in the man page. If all attempts fail, it defaults to using the BASH version.
#### •	get_examples(self)
Provides example usage for the command. This method has a predefined dictionary containing examples for the commands. If the command is in this dictionary, it returns the example; otherwise, it indicates that no example is available.
#### •	get_related_commands(self)
Fetches related commands by using the man -k command. It captures the output and extracts related command names, returning a string of  five related commands separated by ‘\t’, or an error message if no related commands are found.
#### •	get_online_documentation_links(self)
Generates a URL for the online documentation of the command. It returns a link to the command's man page on the Linux documentation website.
#### •	get_recommended_commands(self)
Provides recommendations for related commands. This method has a predefined dictionary containing recommended commands for the commands. It returns a string of  the related commands separated by ‘\t’ or a message indicating no specific recommendations if the command is not in the dictionary.
### 	Class XmlSerializer:
#### •	init(self, manual_data)
Initializes the XmlSerializer instance with the provided manual data. This function sets self.manual_data to the given manual data, which consists of information about a command. It also defines self.output_folder as the destination folder where the XML files will be stored.
#### •	create_xml(self)
Converts the manual data into XML format and saves it as a file. The method first checks if the output folder exists and creates it if it doesn't. It then constructs an XML structure using the ElementTree library, with each key-value pair from the manual data forming part of the XML structure. Finally, the XML data is written to a file, named after the command, in a formatted and readable manner. This method effectively serializes the command manual data into an XML file.
### 	Class ManualVerifier
#### •	init(self, existing_content_path, input_file)
This constructor initializes the ManualVerifier instance with paths to existing content and an input file. The existing_content_path is where previously generated manuals are stored, and input_file is the file containing commands. These paths are set to the respective instance variables.
#### •	verify_manuals(self, commands)
This method verifies the generated command manuals against existing ones. It iterates over the list of commands, generates their manuals using CommandManual, reads existing content, and compares the new content with the existing one. If there's a difference or if the existing content is missing, it records a verification message. The method returns a list of these messages, which indicate the result of the verification for each command.
#### •	read_existing_content(self, command)
Reads and parses the existing XML content for a given command. This method tries to open the XML file corresponding to the command, extract its content, and structure it in a dictionary format similar to the newly generated content. If the file doesn't exist, it returns a message indicating the file was not found.
#### •	compare_content(existing_content, generated_content)
A static method that compares the existing manual content (read from an XML file) with the newly generated manual content. It checks each section of the manual (like description, version history, etc.) and notes any differences. The method returns a detailed message highlighting these differences or a confirmation message if the contents match.
### 	Function get_info_for_selection
This function retrieves specific information about a command based on the user's selection. It is designed to parse an XML file containing detailed data about a command and return information according to the user's choice, such as the command's description, version history, examples, related commands, online documentation links, or recommended commands.





## 	"GUI.py"
This class and its methods mutually build the user interface for the project, handling user interactions, displaying command manual data, and integrating with the backend logic for generating and verifying manuals.
#### •	init(self, master)
Initializes the ManualViewerApp instance. Sets up the main application window (master), configures its title, and initializes variables and widgets. It prepares the user interface for interaction.
#### •	create_widgets(self)
Creates and configures various widgets (like buttons, dropdown lists, text boxes, radio buttons) in the GUI. This includes a button for generating manuals, verifying manuals, a dropdown to select commands, a text box to display manual information, radio buttons for different information choices, and a search button.
#### •	generate_manuals(self)
Invokes the CommandManualGenerator to generate manuals for commands listed in a file ("input_commands.txt"). It handles the process of manual generation and updates the GUI based on the outcome, showing success or error messages as needed.
#### •	display_manual_info(self)
Displays information about the selected command in the manual display text box. It retrieves the command and user choice (from the dropdown and radio buttons), fetches the relevant information, and updates the text box with this information.
#### •	verify_manuals(self)
Verifies the generated manuals using the ManualVerifier class. It checks if the manuals are consistent with existing content or newly generated data, displays success or error messages, and updates the GUI accordingly (like enabling or disabling the search button).
#### •	enable_search_button(self) and disable_search_button(self)
These functions enable or disable the search button and radio buttons based on conditions, like the successful verification of manuals.
#### •	show_message(title, message="", is_error=False)
A static method to display informational or error messages in popup windows. It shows different types of messages (info or error) based on the is_error flag.
#### •	mainloop(self)
Starts the tkinter event loop, which keeps the application running and responsive to user actions.
#### •	main()
This standalone function initializes the tkinter root, creates an instance of ManualViewerApp, and starts the application's main loop.
