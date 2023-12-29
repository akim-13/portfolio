from my_logger import d, i, w, e
import os
import sys
import shlex
import itertools

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
COMPUTER_GENERATED_FILENAME = 'computerGame.txt'

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
        self.output_filename = self.validate_output_file_accessibility(args[2])
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


    def validate_output_file_accessibility(self, filename):
        file_exists = os.path.exists(filename)

        if (file_exists) and (not self._file_has_txt_extension(filename)):
                sys.exit(OUTPUT_FILE_ISSUE)
        else:
            try:
                # Attempt to create the file.
                with open(filename, 'w'):
                    pass
            except IOError:
                print(f'ERROR: The output file "{filename}" cannot be created.')
                sys.exit(OUTPUT_FILE_ISSUE)

        file_is_writable = os.access(filename, os.W_OK)
        if not file_is_writable:
            print(f'ERROR: The output file "{filename}" is not writable.')
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
        self.computer_guesses = []


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
            self._write_to_output_file(self.input_args.output_filename)
            sys.exit(CODE_ISSUE)


    def _write_to_output_file(self, filename):
        with open(filename, 'w') as file:
            for line in self.output_lines:
                file.write(line + '\n')


    def _choose_player_mode(self, player_line):
        player_line = player_line.strip()
        if player_line == 'player human':
            self._process_all_guess_lines()
        elif player_line == 'player computer':
            self._handle_computer_player()
        else:
            self.output_lines.append('No or ill-formed player provided')
            self._write_to_output_file(self.input_args.output_filename)
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
                
        self._write_to_output_file(self.input_args.output_filename)


    def _process_line_of_guesses(self, current_guess_num):
        self.out_of_guesses = (current_guess_num >= len(self.guess_lines)) or (current_guess_num >= self.input_args.maximum_guesses)
        guesses = self._validate_current_guesses(current_guess_num)

        current_line_output = self._generate_guess_based_feedback(guesses, current_guess_num, self.code)
        self.output_lines.append(current_line_output)

        correct_position_guesses = current_line_output.count(CORRECT_POSITION_GUESS)
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


    def _generate_guess_based_feedback(self, guesses, current_guess_num, code):
        current_line_output = f'Guess {current_guess_num}: '
        # Make copies of the lists in order to preserve the originals.
        code_copy = code.copy()
        guesses_copy = guesses.copy()

        # Find all pegs that are in the right position.
        for i, (guess, code_colour) in enumerate(zip(guesses_copy, code_copy)):
            if guess == code_colour:
                current_line_output += CORRECT_POSITION_GUESS + ' '
                # Nullify the current guess and corresponding code to ensure that they are not used later on.
                guesses_copy[i] = None
                code_copy[i] = None

        # Find all the remaining pegs that are in the wrong position but of the right colour.
        for i, code_colour in enumerate(code_copy):
            if (code_colour is not None) and (code_colour in guesses_copy):
                current_line_output += CORRECT_COLOUR_GUESS + ' '
                j = guesses_copy.index(code_colour)
                code_copy[i] = None
                guesses_copy[j] = None

        # Remove the last space only when `current_line_output` has been modified.
        if current_line_output.endswith(f'{CORRECT_POSITION_GUESS} ') or current_line_output.endswith(f'{CORRECT_COLOUR_GUESS} '):
            current_line_output = current_line_output.strip()

        return current_line_output


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


    def _handle_computer_player(self):
        self.input_args.validate_output_file_accessibility(COMPUTER_GENERATED_FILENAME)
        # Create an iterator containing all possible combinations of available colours.
        all_possible_codes = itertools.product(self.input_args.available_colours, repeat=len(self.code))
        initial_guess = self._generate_initial_guess()
        d(f'Initial guess: {initial_guess}')

        correct_position_guesses = 0
        while correct_position_guesses != len(self.code):
            # TODO: Rename `s`.
            possible_codes = itertools.product(self.input_args.available_colours, repeat=len(self.code))
            s = self._remove_wrong_codes(possible_codes, initial_guess)
            possible_codes = itertools.product(self.input_args.available_colours, repeat=len(self.code))
            next_guess = self._generate_next_guess(possible_codes, s)
            current_line_output = self._generate_guess_based_feedback(next_guess, 1, self.code)
            correct_position_guesses = current_line_output.count(CORRECT_POSITION_GUESS)

            d(f'next guess: {next_guess}')

        d('hooray')

    def _generate_next_guess(self, possible_codes, s):
        potential_guesses = []
        min_score = INF

        for guess in possible_codes:
            num_of_pos_and_colour_occurences = {}

            for code in s:
                current_line_output = self._generate_guess_based_feedback(list(guess), 1, code)
                correct_position_guesses = current_line_output.count(CORRECT_POSITION_GUESS)
                correct_colour_guesses = current_line_output.count(CORRECT_COLOUR_GUESS)
                key = (correct_position_guesses, correct_colour_guesses)

                num_of_pos_and_colour_occurences[key] = num_of_pos_and_colour_occurences.get(key, 0) + 1

            max_num_of_occurences = max(num_of_pos_and_colour_occurences.values())
            if max_num_of_occurences < min_score:
                min_score = max_num_of_occurences
                potential_guesses = [guess]
            elif max_num_of_occurences == min_score:
                potential_guesses.append(guess)

        for potential_guess in potential_guesses:
            if potential_guess in s:
                return list(potential_guess)

        return list(potential_guesses[0]) if potential_guesses else None



    # def _generate_next_guess(self, possible_codes, s):
    #     next_guess = None
    #     potential_guesses = []
    #     num_of_pos_and_colour_occurences = {}
    #     scores = {}
    #     for guess in possible_codes:
    #         for code in s:
    #             current_line_output = self._generate_guess_based_feedback(guess, 1, code)
    #             correct_position_guesses = current_line_output.count(CORRECT_POSITION_GUESS)
    #             correct_colour_guesses = current_line_output.count(CORRECT_COLOUR_GUESS)
    #             key = (correct_position_guesses, correct_colour_guesses)
    #             if key not in num_of_pos_and_colour_occurences:
    #                 num_of_pos_and_colour_occurences[key] = 1
    #             else:
    #                 num_of_pos_and_colour_occurences[key] += 1
    #
    #         max_num_of_occurences = max(num_of_pos_and_colour_occurences.values())
    #         scores[guess] = max_num_of_occurences
    #     min_score = min(scores.values())
    #
    #     for guess in possible_codes:
    #         if scores[code] == min_score:
    #             potential_guesses.append(guess)
    #
    #     for potential_guess in potential_guesses:
    #         if potential_guess in s:
    #             next_guess = potential_guess
    #             return next_guess
    #
    #     next_guess = potential_guesses[0]
    #     return next_guess


    def _generate_initial_guess(self):
        initial_guess = []
        color_index = 0
        while len(initial_guess) < len(self.code):
            # Add the same color twice, if possible, before moving to the next color.
            initial_guess.append(self.input_args.available_colours[color_index])
            if len(initial_guess) < len(self.code):
                initial_guess.append(self.input_args.available_colours[color_index])
            
            # Move to the next color and reset to the start if necessary.
            color_index = (color_index + 1) % len(self.input_args.available_colours)

        return initial_guess


    def _remove_wrong_codes(self, possible_codes, guess):
        # TODO: Replace 1, placeholder.
        current_line_output = self._generate_guess_based_feedback(guess, 1, self.code)
        correct_colour_guesses = current_line_output.count(CORRECT_COLOUR_GUESS)
        correct_position_guesses = current_line_output.count(CORRECT_POSITION_GUESS)
        d(f'Guess: {guess}')
        d(f'pos: {correct_position_guesses}')
        d(f'col: {correct_colour_guesses}')
        updated_possible_codes = []
        for possible_code in possible_codes:
            possible_code = list(possible_code)
            current_line_output = self._generate_guess_based_feedback(possible_code, 1, guess)
            current_correct_colour_guesses = current_line_output.count(CORRECT_COLOUR_GUESS)
            current_correct_position_guesses = current_line_output.count(CORRECT_POSITION_GUESS)
            if (current_correct_position_guesses == correct_position_guesses) and (current_correct_colour_guesses == correct_colour_guesses):
                updated_possible_codes.append(possible_code)

        return updated_possible_codes


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
    # except Exception as e:
    #     print(f'UNEXPECTED ERROR:\n{e}')
    #     sys.exit(UNEXPECTED_ERROR)
