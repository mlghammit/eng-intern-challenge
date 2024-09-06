import sys

# Braille to English dictionary
braille_to_english = {
    "O.....": "a", "O.O...": "b", "OO....": "c", "OO.O..": "d", "O..O..": "e",
    "OOO...": "f", "OOOO..": "g", "O.OO..": "h", ".OO...": "i", ".OOO..": "j",
    "O...O.": "k", "O.O.O.": "l", "OO..O.": "m", "OO.OO.": "n", "O..OO.": "o",
    "OOO.O.": "p", "OOOOO.": "q", "O.OOO.": "r", ".OO.O.": "s", ".OOOO.": "t",
    "O...OO": "u", "O.O.OO": "v", ".OOO.O": "w", "OO..OO": "x", "OO.OOO": "y",
    "O..OOO": "z"
}

# Braille to number dictionary
braille_to_number = {
    "O.....": "1", "O.O...": "2", "OO....": "3", "OO.O..": "4", "O..O..": "5",
    "OOO...": "6", "OOOO..": "7", "O.OO..": "8", ".OO...": "9", ".OOO..": "0"
}

# Markers
capital_marker = ".....O" # Indicates following character is uppercase
number_marker = ".O.OOO" # Indicates following characters are numbers
space_marker = "......" # Indicates space in Braile

# Reverse the dictionaries for English to Braille translation
english_to_braille = {v: k for k, v in braille_to_english.items()}
number_to_braille = {v: k for k, v in braille_to_number.items()}

# Precompute valid characters
valid_chars_set = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")

# Function to translate English text to Braile
def englishToBraille(input_string):
    # Check if string is empty
    if not input_string:
        raise ValueError("Empty input string")

    output = [] # Initalizes list to store braille
    is_number = False # Flag if number

    for char in input_string:
        # Valid character, error if not
        if char not in valid_chars_set:
            raise ValueError("Invalid character in input string")

        # Handle uppercase by appending capital marker
        if char.isupper():
            output.append(capital_marker)
            char = char.lower() # convert to lower for translator

        # Handle digits by appending number marker
        if char.isdigit():
            if not is_number:
                output.append(number_marker)
                is_number = True 
            output.append(number_to_braille[char]) 
        elif char == " ":
            # Handle spaces and reset number mode
            output.append(space_marker)
            is_number = False
        else:
            # Handle regular letters to Braille
            output.append(english_to_braille[char])
            is_number = False # Exit number mode 

    return "".join(output) # Return braile translation as a string

# Function to translate Braille to English
def brailleToEnglish(input_string):
    # Check if length of braille input is valid ( Divisble by 6 )
    if len(input_string) % 6 != 0:
        raise ValueError("Invalid Braille string length")

    # Check if empty, edge case
    if not input_string:
        raise ValueError("Empty input string")

    output = [] # List to store english output 
    is_capital = False # Flag for capitalization mode
    is_number = False # Flag for number mode

    # Sliding window approach, process 6-character chunks in one pass
    for i in range(0, len(input_string), 6):
        segment = input_string[i:i+6]

        if segment == space_marker:
            # Handle space and reset number mode
            output.append(" ")
            is_number = False
        elif segment == capital_marker:
            # Set capitalization flag
            is_capital = True
        elif segment == number_marker:
            # Set number mode flag
            is_number = True
        elif is_number:
            # Translate Braille to a number
            output.append(braille_to_number[segment])
        else:
            # Translate Braille to a regular letter, apply capitalization if needed
            char = braille_to_english.get(segment, '')
            output.append(char.upper() if is_capital else char)
            is_capital = False  # Reset capitalization flag after use

    return "".join(output)  # Return the English translation as a string

# Function to determine if input is Braille or English
def translate(input_string):
    # If all characters are 'O' or '.', assume it's Braille
    if all(c in "O." for c in input_string):
        return brailleToEnglish(input_string)
    # Otherwise, assume it's English text and translate to Braille
    return englishToBraille(input_string)

if __name__ == "__main__":
    # Join command-line arguments into a single string to handle spaces correctly
    input_string = " ".join(sys.argv[1:])
    # Translate input and print the result
    output = translate(input_string)
    print(output)
