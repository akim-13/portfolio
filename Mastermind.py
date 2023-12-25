from my_logger import d, i, w, e
import sys
import os
import shlex

# Do not set too high, since the number of possible
# combinations = `num_of_colours**MAX_CODE_LENGTH`.
MAX_CODE_LENGTH = 32
MAX_GUESSES = 65536
DEFAULT_CODE_LENGTH = 5
DEFAULT_MAX_GUESSES = 12
DEFAULT_AVAILABLE_COLOURS = ['red', 'blue', 'yellow', 'green', 'orange']
CORRECT_COLOUR_GUESS = 'white'
CORRECT_POSITION_GUESS = 'black'

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

def write_to_output_file(lines):
    with open(output_filename, 'w') as file:
        for line in lines:
            file.write(line + '\n')


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


def validate_input_file_accessibility(filename):
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


def validate_output_file_accessibility(filename):
    file_exists = os.path.exists(filename)
    file_is_writable = os.access(filename, os.W_OK)

    if file_exists:
        if not file_has_txt_extension(filename):
            sys.exit(OUTPUT_FILE_ISSUE)

        if not file_is_writable:
            print(f'ERROR: The output file "{filename}" is not writable.')
            sys.exit(OUTPUT_FILE_ISSUE)

    else:
        try:
            # Attempt to create the file.
            with open(filename, 'w'):
                pass
        except IOError:
            print(f'ERROR: The output file "{filename}" cannot be created.')
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
    return num


def main(args):
    if len(args) < 3:
        print('ERROR: Not enough arguments provided.')
        print('Usage: python Mastermind.py InputFile OutputFile [CodeLength] [MaximumGuesses] [AvailableColours]*')
        sys.exit(INVALID_ARGS)

    # Make filenames (which never change) global to reduce the number of arguments passed to functions.
    global input_filename, output_filename
    
    input_filename = validate_input_file_accessibility(args[1])
    output_filename = validate_output_file_accessibility(args[2])
    code_length = validate_int_within_bounds(args[3], 1, MAX_CODE_LENGTH) if len(args) > 3 else DEFAULT_CODE_LENGTH
    maximum_guesses = validate_int_within_bounds(args[4], 1, MAX_GUESSES) if len(args) > 4 else DEFAULT_MAX_GUESSES
    # Join the rest of the arguments (available colours) into a string.
    available_colours_str = ' '.join(args[5:]) if len(args) > 5 else ' '.join(DEFAULT_AVAILABLE_COLOURS)
    # Split the string into a list using `shlex` to handle quotes and double quotes like the shell does.
    available_colours = shlex.split(available_colours_str)

    # TODO: Refactor.
    output_lines = []
    with open(input_filename, 'r') as file:
        lines = file.readlines()
        num_of_lines = len(lines)
        if num_of_lines < 2:
            print('ERROR: Ill-formed input file provided.')
            sys.exit(INPUT_FILE_ISSUE)

        code_line = lines[0]
        code_keyword = 'code'
        code_keyword_is_present = code_line.startswith(f'{code_keyword} ')
        # +1 because of the space after the keyword.
        code_keyword_offset = len(code_keyword) + 1
        code = code_line[code_keyword_offset:].strip().split()
        code_is_right_length = len(code) == code_length
        code_colours_are_valid = all(code_colour in available_colours for code_colour in code)
        code_is_valid = code_keyword_is_present and code_is_right_length and code_colours_are_valid
         
        if not code_is_valid:
            output_lines.append('No or ill-formed code provided')
            write_to_output_file(output_lines)
            sys.exit(CODE_ISSUE)

        player_line = lines[1].strip()
        if player_line == 'player human':
            guess_lines = lines[2:]
            no_guesses_provided = guess_lines == []
            if no_guesses_provided:
                output_lines.append('You lost. Please try again.')

            for current_guess_num, line in enumerate(guess_lines, 1):
                guesses = line.strip().split()
                num_of_guesses = len(guesses)
                num_of_guesses_is_correct = num_of_guesses == code_length
                guess_colours_are_valid = all(guess in available_colours for guess in guesses)
                all_guesses_are_valid = num_of_guesses_is_correct and guess_colours_are_valid
                out_of_guesses = current_guess_num >= len(guess_lines) or current_guess_num >= maximum_guesses

                if not all_guesses_are_valid:
                    output_lines.append(f'Guess {current_guess_num}: Ill-formed guess provided')
                    if out_of_guesses:
                        output_lines.append('You lost. Please try again.')
                        break
                    else:
                        continue
                
                current_line_output = f'Guess {current_guess_num}: '

                correct_position_guesses = 0
                for i, code_colour in enumerate(code):
                    for j, guess in enumerate(guesses):
                        if guess == code_colour:
                            if i == j:
                                current_line_output += CORRECT_POSITION_GUESS + ' '
                                correct_position_guesses += 1
                            else:
                                current_line_output += CORRECT_COLOUR_GUESS + ' '
                            guesses[j] = None
                            break

                # Remove the last space only when `current_line_output` has been changed.
                if current_line_output.endswith(f'{CORRECT_POSITION_GUESS} ') or current_line_output.endswith(f'{CORRECT_COLOUR_GUESS} '):
                    current_line_output = current_line_output.strip()

                output_lines.append(current_line_output)

                d(f'cur: {current_guess_num}, max: {maximum_guesses}, len: {len(guess_lines)}')
                if correct_position_guesses == code_length:
                    output_lines.append(f'You won in {current_guess_num} guesses. Congratulations!')
                    if current_guess_num < maximum_guesses:
                        output_lines.append('The game was completed. Further lines were ignored.')
                    break
                elif out_of_guesses:
                    output_lines.append('You lost. Please try again.')
                    break
                    
            write_to_output_file(output_lines)

        elif player_line == 'player computer':
            raise
        else:
            output_lines.append('No or ill-formed player provided')
            write_to_output_file(output_lines)
            sys.exit(PLAYER_ISSUE)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print('\nKEYBOARD INTERRUPT INITIATED.')
        sys.exit(KEYBOARD_INTERRUPT)
    except Exception as e:
        print(f'UNEXPECTED ERROR:\n{e}')
        sys.exit(UNEXPECTED_ERROR)
