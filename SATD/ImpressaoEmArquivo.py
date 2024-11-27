import os


class FileWriter:
    def __init__(self, file_name):
        """
        Initializes the class with the file name and verifies if it already exists.
        If the file exists, asks the user whether to overwrite or specify a new file name.

        :param file_name: Name of the output file.
        """
        self.file_name = file_name
        self.file_handler = None
        self.encoding = "utf-8"  # Define UTF-8 encoding
        self.initialize_file()

    def initialize_file(self):
        """
        Checks if the file exists and prompts the user to overwrite or provide a new name.
        Opens the file for writing after resolving conflicts.
        """
        while True:
            if os.path.exists(self.file_name):
                response = (
                    input(
                        f"The file '{self.file_name}' already exists. Do you want to overwrite it? (y/n): "
                    )
                    .strip()
                    .lower()
                )
                if response == "y":
                    try:
                        self.file_handler = open(
                            self.file_name, "w", encoding=self.encoding
                        )
                        print(
                            f"File '{self.file_name}' has been successfully overwritten."
                        )
                        break
                    except Exception as e:
                        print(f"Error opening file for overwriting: {e}")
                        break
                else:
                    self.file_name = input(
                        "Enter a new name for the file (including the extension): "
                    ).strip()
            else:
                try:
                    self.file_handler = open(
                        self.file_name, "w", encoding=self.encoding
                    )
                    print(f"New file '{self.file_name}' has been successfully created.")
                    break
                except Exception as e:
                    print(f"Error creating the file: {e}")
                    break

    def write_list_to_file(self, data_list):
        """
        Writes each element of the provided list to the file, one per line.

        :param data_list: List of strings to be written to the file.
        """
        if not self.file_handler:
            raise RuntimeError("File handler is not initialized.")

        for line in data_list:
            self.file_handler.write(f"{line}\n")
        # print(f"{len(data_list)} lines have been written to '{self.file_name}'.")

    def close_file(self):
        """
        Closes the file handler if it's open.
        """
        if self.file_handler:
            self.file_handler.close()
            print(f"File '{self.file_name}' has been closed.")
        else:
            print("No file to close.")


def main():
    # Example usage:
    file_writer = FileWriter("output_results.txt")

    # Example list of data to write
    results = [
        "Resultado 1: 123",
        "Resultado 2: 456",
        "Resultado 3: 789",
        "Caracteres especiais: ç, ã, ê, ó, ü",
    ]

    # Write to the file
    file_writer.write_list_to_file(results)

    # Close the file after finishing writing
    file_writer.close_file()


if __name__ == "__main__":
    main()
