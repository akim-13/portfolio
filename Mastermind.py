from my_logger import d, i, w, e
import os
import sys
import shlex

INF = float('inf')

# Do not set too high since the number of possible
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

# TODO: Add docstrings everywhere.

class InputArgs:
    def __init__(self, args):
        self._validate_num_of_args(args)
        self.input_filename  = self._validate_input_file_accessibility(args[1])
        self.output_filename = self._validate_output_file_accessibility(args[2])
        self.code_length     = self.validate_int_within_bounds(args[3], 1, MAX_CODE_LENGTH) if len(args) > 3 else DEFAULT_CODE_LENGTH
        self.maximum_guesses = self.validate_int_within_bounds(args[4], 1, MAX_GUESSES) if len(args) > 4 else DEFAULT_MAX_GUESSES
        # Join the rest of the arguments (available colours) into a string.
        available_colours_str = ' '.join(args[5:]) if len(args) > 5 else ' '.join(DEFAULT_AVAILABLE_COLOURS)
        # Split the string into a list using `shlex` to handle quotes and double quotes like the shell does.
        self.available_colours = shlex.split(available_colours_str)


    @staticmethod
    def _validate_num_of_args(args):
        if len(args) < 3:
            print('ERROR: Not enough arguments provided.')
            print('Usage: python Mastermind.py InputFile OutputFile [CodeLength] [MaximumGuesses] [AvailableColours]*')
            sys.exit(INVALID_ARGS)


    def _validate_input_file_accessibility(self, filename):
        file_exists = os.path.isfile(filename)
        if not file_exists:
            print(f'ERROR: The input file "{filename}" does not exist.')
            sys.exit(INPUT_FILE_ISSUE)

        file_is_readable = os.access(filename, os.R_OK)
        if not file_is_readable:
            print(f'ERROR: The input file "{filename}" is not readable.')
            sys.exit(INPUT_FILE_ISSUE)

        if not self._file_has_txt_extension(filename):
            sys.exit(INPUT_FILE_ISSUE)

        return filename


    @staticmethod
    def _file_has_txt_extension(filename):
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


    def _validate_output_file_accessibility(self, filename):
        file_exists = os.path.exists(filename)
        file_is_writable = os.access(filename, os.W_OK)

        if file_exists:
            if not self._file_has_txt_extension(filename):
                sys.exit(OUTPUT_FILE_ISSUE)

            if not file_is_writable:
                print(f'ERROR: The output file "{filename}" is not writable.')
                sys.exit(OUTPUT_FILE_ISSUE)
        else:
            try:
                # Attempt to create a file.
                with open(filename, 'w'):
                    pass
            except IOError:
                print(f'ERROR: The output file "{filename}" cannot be created.')
                sys.exit(OUTPUT_FILE_ISSUE)

        return filename


    @staticmethod
    def validate_int_within_bounds(num, lower_bound=-INF, upper_bound=INF):
        try:
            num = int(num)
            if num < lower_bound or num > upper_bound:
                print(f'ERROR: {num} is out of bounds (must be between {lower_bound} and {upper_bound}).')
                sys.exit(GENERAL_ERROR)
        except ValueError:
            print(f'ERROR: "{num}" is not an integer.')
            sys.exit(GENERAL_ERROR)
        return num


class ContinueException(Exception):
    """Exception raised to continue in the loop."""
    pass


class BreakException(Exception):
    """Exception raised to break from the loop."""
    pass


class GameProcessor:
    def __init__(self, input_args):
        self.input_args     = input_args
        self.out_of_guesses = True
        self.output_lines   = []
        self.guess_lines    = []
        self.code           = []


    def execute_input_file(self):
        with open(self.input_args.input_filename, 'r') as file:
            lines = file.readlines()
            self._validate_num_of_lines(len(lines))
            self._validate_code(lines[0], 'code')
            player_line = lines[1]
            self.guess_lines = lines[2:]
            self._choose_player_mode(player_line)


    @staticmethod
    def _validate_num_of_lines(num_of_lines):
        if num_of_lines < 2:
            print('ERROR: Ill-formed input file provided.')
            sys.exit(INPUT_FILE_ISSUE)


    def _validate_code(self, code_line, code_keyword):
        code_keyword_is_present = code_line.startswith(f'{code_keyword} ')
        # +1 because of the space after the keyword.
        code_keyword_offset = len(code_keyword) + 1
        self.code = code_line[code_keyword_offset:].strip().split()
        code_is_right_length = len(self.code) == self.input_args.code_length
        code_colours_are_valid = all(code_colour in self.input_args.available_colours for code_colour in self.code)
        code_is_valid = code_keyword_is_present and code_is_right_length and code_colours_are_valid
         
        if not code_is_valid:
            self.output_lines.append('No or ill-formed code provided')
            self._write_to_output_file()
            sys.exit(CODE_ISSUE)


    def _write_to_output_file(self):
        with open(self.input_args.output_filename, 'w') as file:
            for line in self.output_lines:
                file.write(line + '\n')


    def _choose_player_mode(self, player_line):
        player_line = player_line.strip()
        if player_line == 'player human':
            self._process_all_guess_lines()
        elif player_line == 'player computer':
            pass
        else:
            self.output_lines.append('No or ill-formed player provided')
            self._write_to_output_file()
            sys.exit(PLAYER_ISSUE)


    def _process_all_guess_lines(self):
        no_guesses_provided = not self.guess_lines
        if no_guesses_provided:
            self.output_lines.append('You lost. Please try again.')

        for current_guess_num,_ in enumerate(self.guess_lines, 1):
            try:
                self._process_line_of_guesses(current_guess_num)
            except ContinueException:
                continue
            except BreakException:
                break
                
        self._write_to_output_file()


    def _process_line_of_guesses(self, current_guess_num):
        self.out_of_guesses = (current_guess_num >= len(self.guess_lines)) or (current_guess_num >= self.input_args.maximum_guesses)
        guesses = self._validate_current_guesses(current_guess_num)

        (current_line_output, correct_position_guesses) = self._generate_guess_based_feedback(guesses, current_guess_num)
        self.output_lines.append(current_line_output)

        if self._game_is_over(correct_position_guesses, current_guess_num):
            raise BreakException


    def _validate_current_guesses(self, current_guess_num):
        current_guess_line = self.guess_lines[current_guess_num - 1]
        guesses = current_guess_line.strip().split()
        num_of_guesses_is_correct = len(guesses) == self.input_args.code_length
        guess_colours_are_valid = all(guess in self.input_args.available_colours for guess in guesses)
        all_guesses_are_valid = num_of_guesses_is_correct and guess_colours_are_valid

        if not all_guesses_are_valid:
            self.output_lines.append(f'Guess {current_guess_num}: Ill-formed guess provided')
            if self.out_of_guesses:
                self.output_lines.append('You lost. Please try again.')
                raise BreakException
            else:
                raise ContinueException

        return guesses


    def _generate_guess_based_feedback(self, guesses, current_guess_num):
        current_line_output = f'Guess {current_guess_num}: '
        correct_position_guesses = 0
        for i, code_colour in enumerate(self.code):
            for j, guess in enumerate(guesses):
                if guess == code_colour:
                    if i == j:
                        current_line_output += CORRECT_POSITION_GUESS + ' '
                        correct_position_guesses += 1
                    else:
                        current_line_output += CORRECT_COLOUR_GUESS + ' '
                    # Nullify the current guess to ensure that it is not used in further iterations.
                    guesses[j] = None
                    break

        # Remove the last space only when `current_line_output` has been modified.
        if current_line_output.endswith(f'{CORRECT_POSITION_GUESS} ') or current_line_output.endswith(f'{CORRECT_COLOUR_GUESS} '):
            current_line_output = current_line_output.strip()

        return (current_line_output, correct_position_guesses)


    def _game_is_over(self, correct_position_guesses, current_guess_num):
        if correct_position_guesses == self.input_args.code_length:
            self.output_lines.append(f'You won in {current_guess_num} guesses. Congratulations!')
            if not self.out_of_guesses:
                self.output_lines.append('The game was completed. Further lines were ignored.')
            return True
        elif self.out_of_guesses:
            self.output_lines.append('You lost. Please try again.')
            return True
        else:
            return False


def main(args):
    input_args = InputArgs(args)
    game_processor = GameProcessor(input_args)
    game_processor.execute_input_file()


if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print('\nKEYBOARD INTERRUPT INITIATED.')
        sys.exit(KEYBOARD_INTERRUPT)
    except Exception as e:
        print(f'UNEXPECTED ERROR:\n{e}')
        sys.exit(UNEXPECTED_ERROR)
