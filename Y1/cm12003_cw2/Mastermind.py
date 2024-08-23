import re
import os
import sys
import itertools

INF = float('inf')

MAX_CODE_LENGTH = 16
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
UNEXPECTED_ERROR   = 7

class FileHandler():
    """
    Handle file operations such as reading, writing, and validating file accessibility.
    """

    def __init__(self, filename):
        """
        Initialize the `FileHandler` with a specific filename.

        Args:
            `filename` (str): The name of the file to be processed.
        """
        self.filename = filename


    def write_lines_to_file(self, lines):
        """
        Write given lines to the specified file.

        Args:
            `lines` (List[str]): A list of strings, each representing a line to be written to the file.
        """
        with open(self.filename, 'w') as file:
            for line in lines:
                file.write(line + '\n')


    def _file_has_txt_extension(self):
        """
        Check if the file has a .txt extension.

        Return:
            bool: `True` if the file has a .txt extension, `False` otherwise.
        """
        filename_ends_with_txt = self.filename.lower().endswith('.txt')

        if not filename_ends_with_txt:
            print(f'ERROR: The file "{self.filename}" does not have a .txt extension.')
            return False
        else:
            return True


    def validate_input_file_accessibility(self):
        """
        Validate if the input file is accessible and has the correct format.

        Return:
            `self.filename` (str): The filename if validation is successful.
        """
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
        """
        Validate if the output file is accessible and has the correct format.

        Return:
            `self_filename` (str): The filename if validation is successful.
        """
        file_exists = os.path.exists(self.filename)

        if (file_exists) and (not self._file_has_txt_extension()):
                sys.exit(OUTPUT_FILE_ISSUE)

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
    """
    Parse, process and validate command line arguments to set up the game configuration.
    """

    def __init__(self, args):
        """
        Initialize `InputArgs` with command line arguments.

        Args:
            `args` (List[str]): A list of command line arguments.
        """
        num_of_args            = self._validate_num_of_args(args)
        self.input_filename    = FileHandler(args[1]).validate_input_file_accessibility()
        self.output_filename   = FileHandler(args[2]).validate_output_file_accessibility()
        self.code_length       = self._validate_arg_is_valid_int(args[3], 1, MAX_CODE_LENGTH) if num_of_args > 3 else DEFAULT_CODE_LENGTH
        self.max_guesses       = self._validate_arg_is_valid_int(args[4], 1, MAX_GUESSES) if num_of_args > 4 else DEFAULT_MAX_GUESSES
        self.available_colours = self._validate_colours(args[5:]) if num_of_args > 5 else DEFAULT_AVAILABLE_COLOURS


    @staticmethod
    def _validate_num_of_args(args):
        """
        Validate the number of command line arguments provided.

        Args:
            `args` (List[str]): A list of command line arguments.

        Return:
            `num_of_args` (int): The number of arguments.
        """
        num_of_args = len(args)

        if num_of_args < 3:
            print('ERROR: Not enough arguments provided.')
            print('Usage: python Mastermind.py InputFile OutputFile [CodeLength] [MaximumGuesses] [AvailableColours]*')
            sys.exit(INVALID_ARGS)

        return num_of_args


    @staticmethod
    def _validate_arg_is_valid_int(num, lower_bound=-INF, upper_bound=INF):
        """
        Validate whether a provided argument is a valid integer within specified bounds.

        Args:
            `num` (str): The argument to validate as an integer. 
            `lower_bound` (int): The lower bound of the valid range. Defaults to negative infinity.
            `upper_bound` (int): The upper bound of the valid range. Defaults to positive infinity.

        Return:
            `num` (int): The validated integer.
        """
        try:
            num = int(num)
            if num < lower_bound or num > upper_bound:
                print(f'ERROR: {num} is out of bounds (must be between {lower_bound} and {upper_bound}).')
                sys.exit(INVALID_ARGS)
        except ValueError:
            print(f'ERROR: "{num}" is not an integer.')
            sys.exit(INVALID_ARGS)

        return num


    def _validate_colours(self, colours):
        """
        Validate the colours provided in a string and return them as a list.

        Args:
            `colours` (List[str]): A string containing colour names.

        Return:
            `colours` (List[str]): A list of valid colour names.
        """
        # Allow only letters and optionally hyphens, e.g. 'light-green'.
        valid_colour_pattern = re.compile(r'^[a-zA-Z]+(-[a-zA-Z]+)*$')
        all_colours_are_valid = all(valid_colour_pattern.match(colour) for colour in colours)

        if not all_colours_are_valid:
                print(f'ERROR: One or more provided colours are invalid.')
                sys.exit(INVALID_ARGS)

        return colours


class GameProcessor:
    """
    Manage and process the game logic for Mastermind based on input arguments.

    Handle the game's execution flow, processing guesses, generating feedback, 
    and determining the outcome of the game.
    """

    def __init__(self, input_args):
        """
        Initialize `GameProcessor` with the provided input arguments.

        Args:
            `input_args` (InputArgs): An instance of `InputArgs` containing the game configuration.
        """
        self.input_args           = input_args
        self.out_of_guesses       = False
        self.player_mode_is_human = True
        self.output_lines         = []
        self.guess_lines          = []
        self.code                 = []


    def execute_input_file(self):
        """
        Execute the game logic based on the contents of the input file.
        """
        with open(self.input_args.input_filename, 'r') as file:
            lines = file.readlines()
            self._validate_num_of_lines(len(lines))
            self._validate_code(lines[0])
            player_line = lines[1]
            self.guess_lines = lines[2:]
            self._choose_player_mode(player_line)


    @staticmethod
    def _validate_num_of_lines(num_of_lines):
        """
        Validate the number of lines in a file.

        Args:
            `num_of_lines` (int): The number of lines in the file.
        """
        if num_of_lines < 2:
            print('ERROR: Ill-formed input file provided.')
            sys.exit(INPUT_FILE_ISSUE)


    def _validate_code(self, code_line):
        """
        Validate the code line from the input file.

        Args:
            `code_line` (str): The line from the input file containing the code (the secret combination of colours).
        """
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
        """
        Choose the player mode based on the input file's player line.

        Args:
            `player_line` (str): The line from the input file indicating the player mode.
        """
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
        """
        Process all guess lines from the input file in human player mode and write them to the output file.
        """
        no_guesses_provided = not self.guess_lines

        if no_guesses_provided:
            self.output_lines.append('You lost. Please try again.')

        for current_guess_num,_ in enumerate(self.guess_lines, 1):
            correct_position_guesses = self._process_line_of_guesses(current_guess_num)

            if self._game_is_over(correct_position_guesses, current_guess_num):
                break
                
        FileHandler(self.input_args.output_filename).write_lines_to_file(self.output_lines)


    def _process_line_of_guesses(self, current_guess_num):
        """
        Process a single line of guesses.

        Args:
            `current_guess_num` (int): The current guess number.

        Return:
            `correct_position_guesses` (int): The number of pegs in the correct position.
        """
        self.out_of_guesses = (current_guess_num >= len(self.guess_lines)) or (current_guess_num >= self.input_args.max_guesses)
        guesses = self._validate_current_guesses(current_guess_num)

        if not guesses:
            return 0

        current_line_output = self._generate_guess_based_feedback_str(self.code, guesses, current_guess_num)
        self.output_lines.append(current_line_output)
        correct_position_guesses = current_line_output.count(CORRECT_POSITION_GUESS)

        return correct_position_guesses


    def _validate_current_guesses(self, current_guess_num):
        """
        Validate the guesses of the current guess line.

        Args:
            `current_guess_num` (int): The current guess number.

        Return:
            `guesses` (List[str]): A list of valid current line guesses.
        """
        current_guess_line = self.guess_lines[current_guess_num - 1]
        guesses = current_guess_line.strip().split()
        num_of_guesses_is_correct = len(guesses) == self.input_args.code_length
        guess_colours_are_valid = all(guess in self.input_args.available_colours for guess in guesses)
        all_guesses_are_valid = num_of_guesses_is_correct and guess_colours_are_valid

        if not all_guesses_are_valid:
            self.output_lines.append(f'Guess {current_guess_num}: Ill-formed guess provided')
            guesses = []

        return guesses


    def _generate_guess_based_feedback_str(self, code, guesses, current_guess_num):
        """
        Generate a feedback string based on the code and the guesses.

        Args:
            `code` (List[str]): A list of colours against which to check the guesses.
            `guesses` (List[str]): A list of colours as guesses.
            `current_guess_num` (int): The current guess number.

        Return:
            `feedback_string` (str): The feedback string.

        Example:
            Args:
                `code    = ['red', 'blue',  'green']`
                `guesses = ['red', 'green', 'orange']`
                `current_guess_num = 3`
            Return:
                `feedback_string == 'Guess 3: black white'`
        """
        right_pos_count, right_colour_count = self._generate_guess_based_right_pos_col_counts(code, guesses)
        feedback_string = self._assemble_feedback_string(right_pos_count, right_colour_count, current_guess_num)

        return feedback_string


    def _generate_guess_based_right_pos_col_counts(self, code, guesses):
        """
        Generate the counts of right position and right colour pegs (code feedback based on guesses).

        Args:
            `code` (List[str]): A list of colours against which to check the guesses.
            `guesses` (List[str]): A list of colours as guesses.

        Return:
            `right_pos_count, right_colour_count` (Tuple[int, int]): The number of pegs that are in the right position 
                                                                     and the ones that are of the right colour.
        """
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
        """
        Count the number of guesses that are in the correct position.

        Args:
            `code_copy` (List[str]): A copy of the list of colours against which to check the guesses.
            `guesses_copy` (List[str]): A copy of the list of colours as guesses.

        Return:
            `right_pos_count` (int): The number of pegs that are in the right position.
        """
        right_pos_count = 0

        for i, (guess, code_colour) in enumerate(zip(guesses_copy, code_copy)):
            if guess == code_colour:
                right_pos_count += 1
                self._nullify_pegs(code_copy, guesses_copy, i)

        return right_pos_count


    # WARN: Do not call outside `_generate_guess_based_right_pos_col_counts` unless `code_copy` 
    # and `guesses_copy` are copies of the actual variables, they get altered in the process.
    def _generate_right_colour_count(self, code_copy, guesses_copy):
        """
        Count the number of guesses that are of the correct colour but in the wrong position.

        Args:
            `code_copy` (List[str]): A copy of the list of colours against which to check the guesses.
            `guesses_copy` (List[str]): A copy of the list of colours as guesses.

        Return:
            `right_colour_count` (int): The number of pegs that are of the right colour but in the wrong position.
        """
        right_colour_count = 0

        for i, code_colour in enumerate(code_copy):
            if (code_colour is not None) and (code_colour in guesses_copy):
                right_colour_count += 1
                j = guesses_copy.index(code_colour)
                self._nullify_pegs(code_copy, guesses_copy, i, j)

        return right_colour_count


    @staticmethod
    def _nullify_pegs(code, guesses, code_index, guess_index=None):
        """
        Nullify (set to `None`) the pegs at given indices to prevent double counting.

        Args:
            `code` (List[str]): A list of colours against which to check the guesses.
            `guesses` (List[str]): A list of colours as guesses.
            `code_index` (int): The index in the code to nullify.
            `guess_index` (int): The index in the guesses to nullify. Defaults to `None`.
        """
        code[code_index] = None

        if guess_index is not None:
            guesses[guess_index] = None
        else:
            guesses[code_index] = None


    @staticmethod
    def _assemble_feedback_string(right_pos_count, right_colour_count, current_guess_num):
        """
        Assemble the feedback string from counts of right position and colour guesses.

        Args:
            `right_pos_count` (int): The count of right position guesses.
            `right_colour_count` (int): The count of right colour guesses.
            `current_guess_num` (int): The current guess number.

        Return:
            `feedback_string` (str): The assembled feedback string.
        """
        feedback_string = f'Guess {current_guess_num}: '
        feedback_parts = [CORRECT_POSITION_GUESS] * right_pos_count + [CORRECT_COLOUR_GUESS] * right_colour_count
        feedback_string += ' '.join(feedback_parts)

        return feedback_string


    def _game_is_over(self, correct_position_guesses, current_guess_num):
        """
        Check if the game is over based on the number of correct position guesses and the guess number.

        Args:
            `correct_position_guesses` (int): The number of correct position guesses.
            `current_guess_num` (int): The current guess number.

        Return:
            bool: `True` if the game is over, `False` otherwise.
        """
        # `>=` instead of `==` because it is better to be safe than sorry (stuck in an infinite loop).
        if correct_position_guesses >= self.input_args.code_length:
            self.output_lines.append(f'You won in {current_guess_num} guesses. Congratulations!')
            if (self.player_mode_is_human) and (not self.out_of_guesses):
                self.output_lines.append('The game was completed. Further lines were ignored.')
            return True

        elif self.out_of_guesses:
            self.output_lines.append('You lost. Please try again.')
            if current_guess_num == self.input_args.max_guesses:
                self.output_lines.append(f'You can only have {self.input_args.max_guesses} guesses.')
            return True

        else:
            return False


    def _handle_computer_player(self):
        """
        Handle the game logic for the computer player using a generalized version of the Knuth's algorithm.

        The standard Knuth's algorithm is designed for a 4-long code and 6 colours, however this implementation
        generalizes it in order to work with any combination of code length and number of colours. The only 
        limitation is computational power, since the number of available codes grows exponentially with increasing
        code length.
        """
        # Generate all possible codes from the available colours.
        all_possible_codes = itertools.product(self.input_args.available_colours, repeat=len(self.code))
        possible_codes = [ list(code) for code in all_possible_codes ]
        possible_solutions = possible_codes.copy()
        computer_guesses = []
        num_of_combinations = len(possible_codes)
        # `2**14` has been chosen arbitrarily.
        too_many_combinations = num_of_combinations > 2**14

        if too_many_combinations:
            self._warn_user(num_of_combinations)

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
            self.out_of_guesses = current_guess_num == self.input_args.max_guesses

        FileHandler(self.input_args.output_filename).write_lines_to_file(self.output_lines)
        self._write_computer_guesses_to_file(computer_guesses)


    @staticmethod
    def _warn_user(num_of_combinations):
        """
        Warn the user about the potentially long computation time due to a large number of code combinations.

        Args:
            `num_of_combinations` (int): The total number of possible code combinations.
        """
        print(f'There are {num_of_combinations} possible code combinations. This might take a while.')
        user_warning_reply = input('Are you sure you want to proceed? [Y/n] ').lower()

        if user_warning_reply == 'n':
            print('Execution terminated by the user.')
            sys.exit(SUCCESS)


    def _generate_initial_guess(self):
        """
        Generate the initial guess for the computer player.

        The initial guess is created by sequentially picking colors from the available colors list.

        Return:
            `initial_guess` (List[str]): The initial guess.

        Example:
            If:
               `len(self.code) = 5`
               `self.input_args.available_colours = ['R', 'G', 'B', 'Y', 'O', 'P']`
            Then:
                `initial_guess == ['R', 'R', 'G', 'G', 'B']`
        """
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
        """
        Filter possible solutions based on the latest guess and its feedback.

        Compare each possible solution against the latest guess and its feedback
        to narrow down the set of potential solutions.

        Args:
            `possible_solutions` (List[List[str]]): The list of possible solutions.
            `guess` (List[str]): The latest guess made by the computer.

        Return:
            `new_possible_solutions` (List[List[str]]): The filtered list of possible solutions.
        """
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
        """
        Generate the next guess for the computer player.

        Analyze possible codes and solutions to determine the
        most effective next guess using the Minimax algorithm.

        Args:
            `possible_codes` (List[List[str]]): All possible codes.
            `possible_solutions` (List[List[str]]): The list of possible solutions after filtering.

        Return:
            List[str]: The next guess.
        """
        potential_guesses = []
        min_score_of_a_guess = INF

        for guess in possible_codes:
            num_of_pos_and_colour_occurrences = {}
            current_max_occurrences = 0

            for code in possible_solutions:
                pos_and_colour_combo = self._generate_guess_based_right_pos_col_counts(code, guess)
                occurrence_count = num_of_pos_and_colour_occurrences.get(pos_and_colour_combo, 0) + 1
                num_of_pos_and_colour_occurrences[pos_and_colour_combo] = occurrence_count
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
        """
        Write the computer's guesses to a file.

        Args:
            `computer_guesses` (List[List[str]]): The list of guesses made by the computer.
        """
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

