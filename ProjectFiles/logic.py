import os
import subprocess
import xml.etree.ElementTree as ET
from xml.dom import minidom


class CommandManualGenerator:
    def __init__(self, input_file):
        self.input_file = input_file

    def read_commands_from_file(self):
        commands = []
        try:
            with open(self.input_file, 'r') as file:
                for line in file:
                    commands.append(line.strip())
        except FileNotFoundError:
            return f"File not found: {self.input_file}"

        return commands

    def generate_manuals(self):

        commands = self.read_commands_from_file()

        if type(commands) is str:
            return commands

        for command in commands:
            manual = CommandManual(command)
            manual_data = manual.generate_manual()

            xml_serializer = XmlSerializer(manual_data)
            xml_serializer.create_xml()

        return commands


class CommandManual:

    def __init__(self, command):
        self.command = command

    def generate_manual(self):
        description = self.get_command_description()
        version_history = self.get_version_history()
        examples = self.get_examples()
        related_commands = self.get_related_commands()
        online_documentation_links = self.get_online_documentation_links()
        recommended_commands = self.get_recommended_commands()

        return {
            'CommandName': self.command,
            'CommandDescription': description,
            'VersionHistory': version_history,
            'Example': examples,
            'RelatedCommands': related_commands,
            'OnlineDocumentationLinks': online_documentation_links,
            'RecommendedCommands': recommended_commands
        }

    def get_command_description(self):
        try:
            # Try getting description from man page
            man_output = subprocess.check_output(['man', self.command], stderr=subprocess.DEVNULL, text=True)

            description = ''
            start_description = False  # flag if "DESCRIPTION" found

            for line in man_output.split('\n'):

                if start_description:
                    if not line.strip():
                        break  # Stop when an empty line is encountered
                    description += line + '\n'

                elif line.strip() == 'DESCRIPTION':
                    start_description = True

        except subprocess.CalledProcessError:
            try:
                # Try getting description from --help option
                help_output = subprocess.check_output([self.command, '--help'], text=True)

                description = help_output.split('\n')[1]

            except subprocess.CalledProcessError:
                description = f"There is no description for {self.command}"

        return description.strip()

    def get_version_history(self):
        try:
            # Try getting version from --version option
            version_output = subprocess.check_output([self.command, '--version'], stderr=subprocess.DEVNULL, text=True)
            version = version_output.split('\n')[0].split(' ', 1)[1]

        except subprocess.CalledProcessError:
            try:
                # Try getting version from -v option
                version_output = subprocess.check_output([self.command, '-v'], stderr=subprocess.DEVNULL, text=True)
                version = version_output.split('\n')[0].split(' ', 1)[1]

            except subprocess.CalledProcessError:
                try:
                    # Try getting version from man page
                    man_output = subprocess.check_output(['man', self.command], stderr=subprocess.DEVNULL, text=True)
                    version_line = next(line for line in man_output.split('\n') if line.startswith('Version'))
                    version = version_line.split(' ', 1)[1]

                except (subprocess.CalledProcessError, StopIteration):
                    # If all else fails, use the BASH version
                    version = "As the BASH version: " + \
                              subprocess.check_output(['bash', '--version'], text=True).split(' ', 4)[3].split('\n')[0]

        return version.strip()

    def get_examples(self):
        examples = {
            "wc": "wc -l filename.txt",
            "man": "man ls",
            "grep": "grep 'pattern' filename.txt",
            "ls": "ls -l",
            "pwd": "pwd",
            "date": "date '+%Y-%m-%d %H:%M:%S'",
            "who": "who",
            "head": "head -n 5 filename.txt",
            "tr": "tr '[:lower:]' '[:upper:]' < filename.txt",
            "paste": "paste file1.txt file2.txt",
            "tail": "tail -n 10 filename.txt",
            "sed": "sed 's/pattern/replacement/' filename.txt",
            "printf": "printf 'Hello, %s!\\n' 'User'",
            "touch": "touch newfile.txt",
            "pico": "pico filename.txt",
            "mkdir": "mkdir new_directory",
            "cp": "cp file1.txt file2.txt",
            "rm": "rm filename.txt",
            "mv": "mv oldfile.txt newfile.txt",
            "cat": "cat filename.txt"
        }

        return examples.get(self.command, f"No example available for {self.command}")

    def get_related_commands(self):
        try:
            # Run the 'man -k' command and capture the output
            man_output = subprocess.check_output(['man', '-k', self.command], text=True)

            command_names = []
            for line in man_output.split('\n'):
                if line.strip():
                    command_names.append(line.split()[0])

            # Join the related commands with tabs
            related_commands = '\t'.join(command_names[:5])

            return related_commands

        except subprocess.CalledProcessError:
            return f"No related commands found for {self.command}"

    def get_online_documentation_links(self):

        return f"https://linux.die.net/man/1/{self.command}"

    def get_recommended_commands(self):

        recommendations = {
            "ls": ["cd", "cp", "mv"],
            "grep": ["sed", "awk", "cut"],
            "mkdir": ["ls", "cd"],
            "touch": ["ls", "pico", "chmod"],
            "cat": ["grep", "sed", "tr"],
            "wc": ["awk", "sed", "sort"],
            "man": ["info", "apropos"],
            "pwd": ["cd", "ls", "echo"],
            "date": ["cal", "timedatectl"],
            "who": ["w", "finger", "last"],
            "head": ["tail", "sed", "awk"],
            "tr": ["sed", "awk", "cut"],
            "paste": ["join", "sort", "awk"],
            "tail": ["head", "sed", "awk"],
            "sed": ["awk", "grep", "tr"],
            "printf": ["echo", "awk", "printf"],
            "pico": ["nano", "vim", "emacs"],
            "cp": ["mv", "rsync", "scp"],
            "rm": ["mv", "find", "rmdir"],
            "mv": ["cp", "rsync", "scp"]
        }

        if self.command in recommendations:
            recommend = ", ".join(recommendations[self.command])

        else:
            recommend = f"No specific recommendations for '{self.command}'"

        return recommend


class XmlSerializer:
    def __init__(self, manual_data):
        self.manual_data = manual_data
        self.output_folder = "manuals_folder"

    def create_xml(self):
        # Create the output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        manuals = ET.Element("Manuals")

        command_manual = ET.Element("CommandManual")
        for key, value in self.manual_data.items():
            element = ET.SubElement(command_manual, key)
            element.text = value

        manuals.append(command_manual)

        # Save the XML structure to a file with indentation
        file_path = os.path.join(self.output_folder, f"{self.manual_data['CommandName']}_manual.xml")

        xml_str = ET.tostring(manuals, encoding='utf-8').decode()
        xml_str_pretty = minidom.parseString(xml_str).toprettyxml(indent="  ")

        with open(file_path, 'w', encoding='utf-8') as xml_file:
            xml_file.write(xml_str_pretty)


class ManualVerifier:
    def __init__(self, existing_content_path, input_file):
        self.existing_content_path = existing_content_path
        self.input_file = input_file

    def verify_manuals(self, commands):
        verification_messages = []

        if not os.path.exists(self.existing_content_path):
            verification_messages.append("manuals are not generated *_*")
        else:

            for command in commands:
                generator = CommandManual(command)
                existing_content = self.read_existing_content(command)
                generated_content = generator.generate_manual()

                verification_message = self.compare_content(existing_content, generated_content)

                if verification_message is not None:  # Check if verification_message is not None
                    verification_messages.append(verification_message)

        return verification_messages

    def read_existing_content(self, command):
        existing_file_path = os.path.join(self.existing_content_path, f"{command}_manual.xml")

        try:
            # Load the XML file
            tree = ET.parse(existing_file_path)
            root = tree.getroot()

            command_data = {}
            # Iterate through each 'CommandManual' element
            for command_manual_elem in root.findall('CommandManual'):
                # Extract information
                command_data = {
                    'CommandName': command_manual_elem.find('CommandName').text,
                    'CommandDescription': command_manual_elem.find('CommandDescription').text,
                    'VersionHistory': command_manual_elem.find('VersionHistory').text,
                    'Example': command_manual_elem.find('Example').text,
                    'RelatedCommands': command_manual_elem.find('RelatedCommands').text,
                    'OnlineDocumentationLinks': command_manual_elem.find('OnlineDocumentationLinks').text,
                    'RecommendedCommands': command_manual_elem.find('RecommendedCommands').text
                }
        except FileNotFoundError:
            command_data = f"{existing_file_path} not found"

        return command_data

    @staticmethod
    def compare_content(existing_content, generated_content):

        if type(existing_content) is not dict:
            return existing_content

        verification_message = f"\n{existing_content['CommandName']}: "
        error = False
        for key in existing_content.keys():
            existing_value = existing_content.get(key)
            generated_value = generated_content.get(key)

            if existing_value != generated_value:
                error = True
                verification_message += f"{key}: Content has changed\n\n" \
                                        f"  Existing Content: {existing_value}\n\n" \
                                        f"  Generated Content: {generated_value}\n\n"

        if not error:
            verification_message += "verified successfully"

        return verification_message


def get_info_for_selection(command, selection):

    file_path = f"manuals_folder/{command}_manual.xml"

    try:
        # Load the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        command_data = {}
        # Iterate through each 'CommandManual' element
        for command_manual_elem in root.findall('CommandManual'):
            # Extract information
            command_data = {
                    'CommandName': command_manual_elem.find('CommandName').text,
                    'CommandDescription': command_manual_elem.find('CommandDescription').text,
                    'VersionHistory': command_manual_elem.find('VersionHistory').text,
                    'Example': command_manual_elem.find('Example').text,
                    'RelatedCommands': command_manual_elem.find('RelatedCommands').text,
                    'OnlineDocumentationLinks': command_manual_elem.find('OnlineDocumentationLinks').text,
                    'RecommendedCommands': command_manual_elem.find('RecommendedCommands').text
                }

        if selection == "Show All Info":
            keys_to_extract = ['CommandDescription', 'VersionHistory', 'Example', 'RelatedCommands', 'OnlineDocumentationLinks', 'RecommendedCommands']
            formatted_output = ""
            for key in keys_to_extract:
                formatted_output += f"{key}: {command_data[key]}\n\n"

            return formatted_output

        elif selection == "Show Description":
            return f"Command Description: {command_data['CommandDescription']}"

        elif selection == "Show Version":
            return f"Command Version: {command_data['VersionHistory']}"

        elif selection == "Show Example":
            return f"Command Example: {command_data['Example']}"

        elif selection == "Show Related Commands":
            return f"Command Related Commands: {command_data['RelatedCommands']}"

        elif selection == "Show Online Documentation Links":
            return f"Command Online Documentation Links: {command_data['OnlineDocumentationLinks']}"

        elif selection == "Show Recommended Commands":
            return f"Command Recommended Commands: {command_data['RecommendedCommands']}"

        else:
            return f"Invalid selection: {selection}"

    except FileNotFoundError:
        return f"File not found: {file_path}"
