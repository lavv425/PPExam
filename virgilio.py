import os
from typing import List, Union
from json import dump

class CantoNotFoundError(Exception):
    """Custom exception to handle errors related to chant numbers."""
    pass


class Virgilio:
    """Class to manage read operations on Dante's 34 chants."""

    __directory: str

    def __init__(self, directory: str) -> None:
        """
        Initializes an instance of the Virgilio class.

        :param directory: Absolute path of the directory containing the 34 chants.
        """

        if not os.path.isdir(directory):
            raise ValueError(f"Directory '{directory}' does not exist")

        self.__directory = directory

    def get_readable_type(self, of: any) -> str:
        """
        Returns the readable type of the given parameter.

        :param of: The object to get the readable type of.
        :return: The readable type of the given parameter.
        """

        return type(of).__name__

    # Ex 1, 13, 14, arranged to be used in all the other methods
    def read_canto_lines(self, canto_number: int, strip_lines: bool = False, num_lines: Union[int, None] = None) -> Union[List[str], str]:
        """
        Read the specified chant, defined with "canto_number"

        :param canto_number: The chant number (1-34).
        :param strip_lines: If True, removes leading and trailing whitespace from each line.
        :param num_lines: Number of lines to read. None to read the entire file.
        :return: List of lines read from the file or an error message string.
        :raises TypeError: If canto_number is not an integer.
        :raises CantoNotFoundError: If the canto_number is outside the range 1-34.
        :raises Exception: If an error occurs while opening the file.
        """

        if not isinstance(canto_number, int):
            raise TypeError("canto_number must be an integer")
        if not (1 <= canto_number <= 34):
            raise CantoNotFoundError("canto_number must be between 1 and 34")

        file_path: str = os.path.join(
            self.__directory, f"Canto_{canto_number}.txt")

        try:
            with open(file_path, 'r', encoding='utf-8') as chant:
                lines = chant.readlines()
                if strip_lines:
                    lines = [line.strip() for line in lines]
                if num_lines is not None:
                    lines = lines[:num_lines]
                return lines
        except Exception:
            return f"error while opening {file_path}"

    # Ex 2
    def count_verses(self, canto_number: int) -> int:
        """
        Counts the number of verses (lines) in the specified chant.

        :param canto_number: The chant number (1-34).
        :return: The number of verses (lines) in the chant.
        :raises TypeError: If canto_number is not an integer.
        :raises CantoNotFoundError: If canto_number is outside the range 1-34.
        :raises Exception: If an error occurs while opening the file.
        """

        lines = self.read_canto_lines(canto_number)
        if isinstance(lines, str):  # Handle error messages returned by read_canto_lines
            raise Exception(f"Error reading chant {canto_number}: {lines}")
        return len(lines)

    # Ex 3
    def count_tercets(self, canto_number: int) -> int:
        """
        Counts the number of tercets (groups of three verses) in the specified chant.

        :param canto_number: The chant number (1-34).
        :return: The number of tercets in the chant.
        :raises TypeError: If canto_number is not an integer.
        :raises CantoNotFoundError: If canto_number is outside the range 1-34.
        :raises Exception: If an error occurs while opening the file.
        """

        # Get the n of verses using count_verses
        num_verses = self.count_verses(canto_number)
        # Calculate the tercets by integer division
        num_tercets = num_verses // 3
        return num_tercets

    # Ex 4
    def count_word(self, canto_number: int, word: str) -> int:
        """
        Counts the number of occurrences of the specified word in the specified chant.

        :param canto_number: The chant number (1-34).
        :param word: The word (or char) to count. (case-sensitivev)
        :return: The number of occurrences of the word in the chant.
        :raises TypeError: If canto_number is not an integer.
        :raises CantoNotFoundError: If canto_number is outside the range 1-34.
        :raises Exception: If an error occurs while opening the file.
        """

        if not isinstance(word, str):
            raise TypeError(f"word must be of type string, is {self.get_readable_type(word)}")

        lines = self.read_canto_lines(canto_number)
        if isinstance(lines, str):  # Handle error messages returned by read_canto_lines
            raise Exception(f"Error reading chant {canto_number}: {lines}")

        # Combine all lines into a single string, to count word occurence easily
        single_line_chant = "".join(lines)

        return single_line_chant.count(word)

    # Ex 5
    def get_verse_with_word(self, canto_number: int, word: str) -> Union[str, None]:
        """
        Finds and returns the first found verse containing the specified word in the specified chant.

        :param canto_number: The chant number (1-34).
        :param word: The word (or char) to search for. (case-sensitive)
        :return: The first verse containing the word, or None if not found.
        :raises TypeError: If canto_number is not an integer.
        :raises CantoNotFoundError: If canto_number is outside the range 1-34.
        :raises Exception: If an error occurs while opening the file.
        """

        if not isinstance(word, str):
            raise TypeError(f"word must be of type string, is {self.get_readable_type(word)}")

        lines = self.read_canto_lines(canto_number, strip_lines=True)
        if isinstance(lines, str):  # Handle error messages returned by read_canto_lines
            raise Exception(f"Error reading chant {canto_number}: {lines}")

        # Search for the word in the lines
        for line in lines:
            if word in line:
                # return word + line # Using the searched letter/word to concat to the result
                return line

        # If the word was not found in any verse, return None
        return None

    # Ex 6
    def get_verses_with_word(self, canto_number: int, word: str) -> Union[List[str], None]:
        """
        Finds and returns all verses containing the specified word in the specified chant.

        :param canto_number: The chant number (1-34).
        :param word: The word (or char) to search for. (case-sensitive)
        :return: A list of verses containing the word, or an empty list if not found.
        :raises TypeError: If canto_number is not an integer.
        :raises CantoNotFoundError: If canto_number is outside the range 1-34.
        :raises Exception: If an error occurs while opening the file.
        """

        if not isinstance(word, str):
            raise TypeError(f"word must be of type string, is {self.get_readable_type(word)}")

        lines = self.read_canto_lines(canto_number, strip_lines=True)
        if isinstance(lines, str):  # Handle error messages returned by read_canto_lines
            raise Exception(f"Error reading chant {canto_number}: {lines}")

        # Find and return all the verses containing the word
        return [line for line in lines if word in line] or None

    # Ex 7
    def get_longest_verse(self, canto_number: int) -> Union[str, None]:
        """
        Finds and returns the longest verse in the specified chant.
        If more than one verse is found it returns the first one

        :param canto_number: The chant number (1-34).
        :return: The longest verse in the chant, or None if no verses found.
        :raises TypeError: If canto_number is not an integer.
        :raises CantoNotFoundError: If canto_number is outside the range 1-34.
        :raises Exception: If an error occurs while opening the file.
        """

        lines = self.read_canto_lines(canto_number, strip_lines=True)
        if isinstance(lines, str):  # Handle error messages returned by read_canto_lines
            raise Exception(f"Error reading chant {canto_number}: {lines}")

        return max(lines, key=len, default=None)

    # Ex 8
    def get_longest_canto(self) -> dict:
        """
        Finds and returns the chant with the longest verse.

        :return: A dictionary with:
             - "canto_number": The number of the chant with the most verses (int).
             - "canto_len": The number of verses in that chant (int).
        :raises Exception: If an error occurs while reading the chants.
        """

        longest_chant = {
            "canto_number": None,
            "canto_len": 0
        }

        for canto_number in range(1, 35):  # Loop through all the 34 chants
            try:
                # Number of verses in the current chant
                num_verses = self.count_verses(canto_number)
                # Update the longest chant if this chant has more verses
                if num_verses > longest_chant["canto_len"]:
                    longest_chant["canto_number"] = canto_number
                    longest_chant["canto_len"] = num_verses
            except Exception as e:
                # Skip chants that throws errors but log the isssue in the "console"
                print(f"Error processing Canto {canto_number}: {e}")

        return longest_chant

    # Ex 9
    def count_words(self, canto_number: int, words: List[str]) -> dict:
        """
        Counts the occurrences of the specified words in the specified chant.

        :param canto_number: The chant number (1-34).
        :param words: The words (or chars) to search for. (case-sensitive)
        :return: A dictionary with:
             - The specified words as keys.
             - The number of occurrences of each word in the chant as values.
        :raises TypeError: If canto_number is not an integer, or if param words is not a list of strings.
        :raises CantoNotFoundError: If canto_number is outside the range 1-34.
        :raises Exception: If an error occurs while opening the file.
        """
        if not isinstance(words, list) or not all(isinstance(word, str) for word in words):
            raise TypeError(f"words must be a list of strings, is {self.get_readable_type(words)}")

        lines = self.read_canto_lines(canto_number, strip_lines=True)
        if isinstance(lines, str):  # Handle error messages returned by read_canto_lines
            raise Exception(f"Error reading chant {canto_number}: {lines}")

        # Lines into a single string for easier word counting
        full_text = "".join(lines)

        # Count occurrences for each word
        word_counts: dict = {word: full_text.count(word) for word in words}

        output_json_name: str = "word_counts.json"
        try:
            with open(output_json_name, "w", encoding="utf-8") as json_file:
                dump(word_counts, json_file, ensure_ascii=False, indent=4) # 4 indent is a tab
        except Exception as e:
            raise Exception(f"Error writing to JSON file {output_json_name}: {e}")
        
        return word_counts

    # Ex 10
    def get_hell_verses(self) -> List[str]:
        """
        Finds and returns all verses containing All versers from all 34 chants in order as they are read (1 to 34)

        :return: A list of all verses from the Inferno.
        :raises Exception: If an error occurs while reading the chants.
        """

        hell_verses: List[str] = []
        for canto_number in range(1, 35):
            try:
                lines: List[str] | str = self.read_canto_lines(canto_number, strip_lines=True)
                if isinstance(lines, str):  # Handle error messages returned by read_canto_lines
                    raise Exception(f"Error reading chant {canto_number}: {lines}")

                # Add the verses to the list if no error is raised
                hell_verses.extend(lines)
            except Exception as e:
                # Skip chants that throws errors but log the isssue in the "console"
                print(f"Error processing Canto {canto_number}: {e}")

        return hell_verses

    
    # Ex 11
    def count_hell_verses(self) -> int:
        """
        Counts the total number of verses in all 34 chants of the Inferno.

        :return: The total number of verses in the Inferno.
        :raises Exception: If an error occurs while reading a chant.
        """

        total_verses: int = 0

        for canto_number in range(1, 35):
            try:
                # Get the number of verses in the current chant
                num_verses: int = self.count_verses(canto_number)
                total_verses += num_verses  # Add the number of verses to the total
            except Exception as e:
                print(f"Error processing Chant {canto_number}: {e}")

        return total_verses


    # Ex 12
    def get_hell_verse_mean_len(self) -> float:
        """
        Calculates and returns the average length of verses in all 34 chants of the Inferno.

        :return: The average length of verses in the Inferno.
        :raises Exception: If an error occurs while reading a chant.
        """

        total_verses: int = self.count_hell_verses()
        total_verses_len: int = 0

        if total_verses == 0:  # Early return, no verses "available" or found
            return 0.0
    
        for canto_number in range(1, 35):
            try:
                verses: List[str] | str = self.read_canto_lines(canto_number, strip_lines=True)
                if isinstance(verses, str):  # Handle error messages returned by read_canto_lines
                    raise Exception(f"Error reading chant {canto_number}: {verses}")

                total_verses_len += sum(len(verse) for verse in verses)
            except Exception as e:
                print(f"Error processing Canto {canto_number}: {e}")
        
        return total_verses_len / total_verses


directory: str = os.path.join(os.path.dirname(__file__), "chants")
v = Virgilio(directory)

try:
    result = v.count_words(1, ["f", "g", "d", "canto", "inferno"])
    print(result)
except CantoNotFoundError as cnfe:
    print(f"The chant was not found: {cnfe}")
except Exception as e:
    print(f"An error occurred: {e}")
