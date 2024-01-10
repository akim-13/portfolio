from my_logger import d, i, w, e
import os
import sys
import shlex
import itertools

INF = float('inf')

# Do not set too high since the number of possible
# combinations = `num_of_colours**MAX_CODE_LENGTH`.
MAX_CODE_LENGTH = 8
MAX_GUESSES = 1024
DEFAULT_CODE_LENGTH = 5
DEFAULT_MAX_GUESSES = 12
DEFAULT_AVAILABLE_COLOURS = ['red', 'blue', 'yellow', 'green', 'orange']
CORRECT_COLOUR_GUESS = 'white'
CORRECT_POSITION_GUESS = 'black'

CODE_KEYWORD = 'code'
HUMAN_PLAYER_KEYWORDS = 'player human'
COMPUTER_PLAYER_KEYWORDS = 'player computer'
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

class FileHandler():
    def __init__(self, filename):
        self.filename = filename


    def write_lines_to_file(self, lines):
        with open(self.filename, 'w') as file:
            for line in lines:
                file.write(line + '\n')


    def _file_has_txt_extension(self):
        try:
            filename_ends_with_txt = self.filename.lower().endswith('.txt')
        except:
            print(f'ERROR: Invalid filename or file does not exist.')
            sys.exit(GENERAL_ERROR)

        if not filename_ends_with_txt:
            print(f'ERROR: The file "{self.filename}" does not have a .txt extension.')
            return False
        else:
            return True


    def validate_input_file_accessibility(self):
        file_exists = os.path.isfile(self.filename)
        if not file_exists:
            print(f'ERROR: The input file "{self.filename}" does not exist.')
            sys.exit(INPUT_FILE_ISSUE)

        file_is_readable = os.access(self.filename, os.R_OK)
        if not file_is_readable:
            print(f'ERROR: The input file "{self.filename}" is not readable.')
            sys.exit(INPUT_FILE_ISSUE)

        if not self._file_has_txt_extension():
            sys.exit(INPUT_FILE_ISSUE)

        return self.filename


    def validate_output_file_accessibility(self):
        file_exists = os.path.exists(self.filename)

        if (file_exists) and (not self._file_has_txt_extension()):
                sys.exit(OUTPUT_FILE_ISSUE)
        else:
            try:
                # Attempt to create the file.
                with open(self.filename, 'w'):
                    pass
            except IOError:
                print(f'ERROR: The output file "{self.filename}" cannot be created.')
                sys.exit(OUTPUT_FILE_ISSUE)

        file_is_writable = os.access(self.filename, os.W_OK)
        if not file_is_writable:
            print(f'ERROR: The output file "{self.filename}" is not writable.')
            sys.exit(OUTPUT_FILE_ISSUE)

        return self.filename


class InputArgs:
    def __init__(self, args):
        self._validate_num_of_args(args)
        self.input_filename  = FileHandler(args[1]).validate_input_file_accessibility()
        self.output_filename = FileHandler(args[2]).validate_output_file_accessibility()
        self.code_length     = self._validate_arg_is_valid_int(args[3], 1, MAX_CODE_LENGTH) if len(args) > 3 else DEFAULT_CODE_LENGTH
        self.maximum_guesses = self._validate_arg_is_valid_int(args[4], 1, MAX_GUESSES) if len(args) > 4 else DEFAULT_MAX_GUESSES
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


    @staticmethod
    def _validate_arg_is_valid_int(num, lower_bound=-INF, upper_bound=INF):
        try:
            num = int(num)
            if num < lower_bound or num > upper_bound:
                print(f'ERROR: {num} is out of bounds (must be between {lower_bound} and {upper_bound}).')
                sys.exit(INVALID_ARGS)
        except ValueError:
            print(f'ERROR: "{num}" is not an integer.')
            sys.exit(INVALID_ARGS)
        return num


class ContinueException(Exception):
    """Exception raised to continue in a loop."""
    pass


class BreakException(Exception):
    """Exception raised to break from a loop."""
    pass


class GameProcessor:
    def __init__(self, input_args):
        self.input_args           = input_args
        self.out_of_guesses       = False
        self.player_mode_is_human = True
        self.output_lines         = []
        self.guess_lines          = []
        self.code                 = []


    def execute_input_file(self):
        with open(self.input_args.input_filename, 'r') as file:
            lines = file.readlines()
            self._validate_num_of_lines(len(lines))
            self._validate_code(lines[0])
            player_line = lines[1]
            self.guess_lines = lines[2:]
            self._choose_player_mode(player_line)


    @staticmethod
    def _validate_num_of_lines(num_of_lines):
        if num_of_lines < 2:
            print('ERROR: Ill-formed input file provided.')
            sys.exit(INPUT_FILE_ISSUE)


    def _validate_code(self, code_line):
        code_keyword_is_present = code_line.startswith(f'{CODE_KEYWORD} ')
        # +1 because of the space after the keyword.
        code_keyword_offset = len(CODE_KEYWORD) + 1
        self.code = code_line[code_keyword_offset:].strip().split()
        code_is_right_length = len(self.code) == self.input_args.code_length
        code_colours_are_valid = all(code_colour in self.input_args.available_colours for code_colour in self.code)
        code_is_valid = code_keyword_is_present and code_is_right_length and code_colours_are_valid
         
        if not code_is_valid:
            self.output_lines.append('No or ill-formed code provided')
            FileHandler(self.input_args.output_filename).write_lines_to_file(self.output_lines)
            sys.exit(CODE_ISSUE)


    def _choose_player_mode(self, player_line):
        player_line = player_line.strip()
        if player_line == HUMAN_PLAYER_KEYWORDS:
            self._process_all_guess_lines()
        elif player_line == COMPUTER_PLAYER_KEYWORDS:
            self.player_mode_is_human = False
            self._handle_computer_player()
        else:
            self.output_lines.append('No or ill-formed player provided')
            FileHandler(self.input_args.output_filename).write_lines_to_file(self.output_lines)
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
                
        FileHandler(self.input_args.output_filename).write_lines_to_file(self.output_lines)


    def _process_line_of_guesses(self, current_guess_num):
        self.out_of_guesses = (current_guess_num >= len(self.guess_lines)) or (current_guess_num >= self.input_args.maximum_guesses)
        guesses = self._validate_current_guesses(current_guess_num)

        current_line_output = self._generate_guess_based_feedback_str(self.code, guesses, current_guess_num)
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


    def _generate_guess_based_feedback_str(self, code, guesses, current_guess_num):
        right_pos_count, right_colour_count = self._generate_guess_based_right_pos_col_counts(code, guesses)
        feedback_str = self._assemble_feedback_string(right_pos_count, right_colour_count, current_guess_num)

        return feedback_str


    def _generate_guess_based_right_pos_col_counts(self, code, guesses):
        if not (code and guesses):
            return 0, 0

        code_copy = code.copy()
        guesses_copy = guesses.copy()
        right_pos_count = self._generate_right_pos_count(code_copy, guesses_copy)
        right_colour_count = self._generate_right_colour_count(code_copy, guesses_copy)

        return right_pos_count, right_colour_count


    # WARN: Do not call outside `_generate_guess_based_right_pos_col_counts` unless `code_copy` 
    # and `guesses_copy` are copies of the actual variables, they get altered in the process.
    def _generate_right_pos_count(self, code_copy, guesses_copy):
        right_pos_count = 0

        for i, (guess, code_colour) in enumerate(zip(guesses_copy, code_copy)):
            if guess == code_colour:
                right_pos_count += 1
                self._nullify_pegs(code_copy, guesses_copy, i)

        return right_pos_count


    # WARN: Do not call outside `_generate_guess_based_right_pos_col_counts` unless `code_copy` 
    # and `guesses_copy` are copies of the actual variables, they get altered in the process.
    def _generate_right_colour_count(self, code_copy, guesses_copy):
        right_colour_count = 0

        for i, code_colour in enumerate(code_copy):
            if (code_colour is not None) and (code_colour in guesses_copy):
                right_colour_count += 1
                j = guesses_copy.index(code_colour)
                self._nullify_pegs(code_copy, guesses_copy, i, j)

        return right_colour_count


    @staticmethod
    def _nullify_pegs(code, guesses, code_index, guess_index=None):
        """Nullifies the pegs at given indices to prevent double counting."""
        code[code_index] = None

        if guess_index is not None:
            guesses[guess_index] = None
        else:
            guesses[code_index] = None


    @staticmethod
    def _assemble_feedback_string(right_pos_count, right_colour_count, current_guess_num):
        feedback_string = f'Guess {current_guess_num}: '
        feedback_parts = [CORRECT_POSITION_GUESS] * right_pos_count + [CORRECT_COLOUR_GUESS] * right_colour_count
        feedback_string += ' '.join(feedback_parts)

        return feedback_string


    def _game_is_over(self, correct_position_guesses, current_guess_num):
        # `>=` instead of `==` because it is better to be safe than sorry (stuck in an infinite loop).
        if correct_position_guesses >= self.input_args.code_length:
            self.output_lines.append(f'You won in {current_guess_num} guesses. Congratulations!')
            if (self.player_mode_is_human) and (not self.out_of_guesses):
                self.output_lines.append('The game was completed. Further lines were ignored.')
            return True
        elif self.out_of_guesses:
            self.output_lines.append('You lost. Please try again.')
            return True
        else:
            return False


    def _handle_computer_player(self):
        # Generate all possible codes from the available colours.
        all_possible_codes = itertools.product(self.input_args.available_colours, repeat=len(self.code))
        possible_codes = [ list(code) for code in all_possible_codes ]
        possible_solutions = possible_codes.copy()
        computer_guesses = []

        print('Generating solutions...')

        current_guess = self._generate_initial_guess()
        current_guess_num = 1

        while True:
            computer_guesses.append(current_guess)

            current_line_output = self._generate_guess_based_feedback_str(self.code, current_guess, current_guess_num)
            self.output_lines.append(current_line_output)
            correct_position_guesses = current_line_output.count(CORRECT_POSITION_GUESS)

            if self._game_is_over(correct_position_guesses, current_guess_num):
                break

            possible_solutions = self._filter_possible_solutions(possible_solutions, current_guess)
            current_guess = self._generate_next_guess(possible_codes, possible_solutions)
            current_guess_num += 1
            self.out_of_guesses = current_guess_num == self.input_args.maximum_guesses

        FileHandler(self.input_args.output_filename).write_lines_to_file(self.output_lines)
        self._write_computer_guesses_to_file(computer_guesses)


    def _generate_initial_guess(self):
        initial_guess = []
        colour_index = 0
        finished_generating_initial_guess = False

        while not finished_generating_initial_guess:
            # Add the same colour twice, if possible, before moving to the next colour.
            initial_guess.append(self.input_args.available_colours[colour_index])
            finished_generating_initial_guess = len(initial_guess) >= len(self.code)
            if not finished_generating_initial_guess:
                initial_guess.append(self.input_args.available_colours[colour_index])
            
            # Move to the next colour and reset to the start if necessary.
            colour_index = (colour_index + 1) % len(self.input_args.available_colours)

        return initial_guess


    def _filter_possible_solutions(self, possible_solutions, guess):
        new_possible_solutions = []

        if not self.output_lines:
            return new_possible_solutions

        current_line_output = self.output_lines[-1]
        correct_position_guesses = current_line_output.count(CORRECT_POSITION_GUESS)
        correct_colour_guesses = current_line_output.count(CORRECT_COLOUR_GUESS)

        for possible_solution in possible_solutions:
            current_correct_position_guesses, current_correct_colour_guesses = self._generate_guess_based_right_pos_col_counts(guess, possible_solution)

            feedback_is_the_same = (current_correct_position_guesses == correct_position_guesses) and (current_correct_colour_guesses == correct_colour_guesses)
            if feedback_is_the_same:
                new_possible_solutions.append(possible_solution)

        return new_possible_solutions


    def _generate_next_guess(self, possible_codes, possible_solutions):
        potential_guesses = []
        min_score_of_a_guess = INF

        for guess in possible_codes:
            num_of_pos_and_colour_occurrences = {}
            current_max_occurrences = 0

            for code in possible_solutions:
                pos_and_color_combo = self._generate_guess_based_right_pos_col_counts(code, guess)
                occurrence_count = num_of_pos_and_colour_occurrences.get(pos_and_color_combo, 0) + 1
                num_of_pos_and_colour_occurrences[pos_and_color_combo] = occurrence_count
                current_max_occurrences = max(current_max_occurrences, occurrence_count)

            if current_max_occurrences < min_score_of_a_guess:
                min_score_of_a_guess = current_max_occurrences
                potential_guesses = [guess]
            elif current_max_occurrences == min_score_of_a_guess:
                potential_guesses.append(guess)

        # It is preferable for a guess to be a possible solution, but not necessary.
        for potential_guess in potential_guesses:
            if potential_guess in possible_solutions:
                return potential_guess

        return potential_guesses[0] if potential_guesses else None


    def _write_computer_guesses_to_file(self, computer_guesses):
        FileHandler(COMPUTER_GENERATED_FILENAME).validate_output_file_accessibility()

        computer_aux_file_lines = []
        code_line = f'{CODE_KEYWORD} {" ".join(self.code)}'
        computer_guess_lines = [ ' '.join(guess) for guess in computer_guesses ]
        computer_aux_file_lines += [code_line, HUMAN_PLAYER_KEYWORDS] + computer_guess_lines

        FileHandler(COMPUTER_GENERATED_FILENAME).write_lines_to_file(computer_aux_file_lines)


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
