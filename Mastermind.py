from my_logger import d, i, w, e
import sys
import os

# Do not set too high, since the number of possible
# combinations = `num_of_colours**MAX_CODE_LENGTH`.
MAX_CODE_LENGTH = 32
MAX_GUESSES = 65536
DEFAULT_CODE_LENGTH = 5
DEFAULT_MAX_GUESSES = 12
DEFAULT_AVAILABLE_COLOURS = ['red', 'blue', 'yellow', 'green', 'orange']

# Define exit codes as constants for clarity.
SUCCESS            = 0
INVALID_ARGS       = 1
INPUT_FILE_ISSUE   = 2
OUTPUT_FILE_ISSUE  = 3
CODE_ISSUE         = 4
PLAYER_ISSUE       = 5
KEYBOARD_INTERRUPT = 6
GENERAL_ERROR      = 7
UNEXPECTED_ERROR   = 8

def file_has_txt_extension(filename):
    try:
        filename_ends_with_txt = filename.lower().endswith('.txt')
    except:
        print(f'ERROR: Invalid filename or file does not exist.')
        sys.exit(GENERAL_ERROR)

    if not filename_ends_with_txt:
        print(f'ERROR: The file "{filename}" does not have a .txt extension.')
        return False
    else:
        return True


def validate_input_file(filename):
    file_exists = os.path.isfile(filename)
    if not file_exists:
        print(f'ERROR: The input file "{filename}" does not exist.')
        sys.exit(INPUT_FILE_ISSUE)

    file_is_readable = os.access(filename, os.R_OK)
    if not file_is_readable:
        print(f'ERROR: The input file "{filename}" is not readable.')
        sys.exit(INPUT_FILE_ISSUE)

    if not file_has_txt_extension(filename):
        sys.exit(INPUT_FILE_ISSUE)

    return filename


def validate_output_file(filename):
    file_exists = os.path.exists(filename)
    file_is_writable = os.access(filename, os.W_OK)

    if file_exists:
        if not file_has_txt_extension(filename):
            sys.exit(OUTPUT_FILE_ISSUE)

        if not file_is_writable:
            print(f'ERROR: The output file {filename} is not writable.')
            sys.exit(OUTPUT_FILE_ISSUE)

    else:
        try:
            # Attempt to create the file.
            with open(filename, 'w'):
                pass
        except IOError:
            print(f'ERROR: The output file {filename} cannot be created.')
            sys.exit(OUTPUT_FILE_ISSUE)

    return filename


def validate_int_within_bounds(num, lower_bound, upper_bound):
    try:
        num = int(num)
        if num < lower_bound or num > upper_bound:
            print(f'ERROR: {num} is out of bounds (must be between {lower_bound} and {upper_bound}).')
            sys.exit(GENERAL_ERROR)
    except ValueError:
        print(f'ERROR: "{num}" is not an integer.')
        sys.exit(GENERAL_ERROR)


def main(args):
    if len(args) < 3:
        print('ERROR: Not enough arguments provided.')
        print('Usage: python Mastermind.py InputFile OutputFile [CodeLength] [MaximumGuesses] [AvailableColours]*')
        sys.exit(INVALID_ARGS)
    
    input_file = validate_input_file(args[1])
    output_file = validate_output_file(args[2])
    code_length = validate_int_within_bounds(args[3], 1, MAX_CODE_LENGTH) if len(args) > 3 else DEFAULT_CODE_LENGTH
    maximum_guesses = validate_int_within_bounds(args[4], 1, MAX_GUESSES) if len(args) > 4 else DEFAULT_MAX_GUESSES
    available_colours = args[5:] if len(args) > 5 else DEFAULT_AVAILABLE_COLOURS

    
if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print('\nKEYBOARD INTERRUPT INITIATED.')
        sys.exit(KEYBOARD_INTERRUPT)
    except Exception as e:
        print(f'UNEXPECTED ERROR:\n{e}')
        sys.exit(UNEXPECTED_ERROR)
