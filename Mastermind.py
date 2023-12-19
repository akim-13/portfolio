from my_logger import d, i, w, e
import sys

def main(args):
    int('hi')
    # Check the number of arguments
    if len(args) < 2:
        print('Usage: python Mastermind.py InputFile OutputFile [CodeLength] [MaximumGuesses] [AvailableColours]')
        sys.exit(1)
    
    input_file = args[1]
    output_file = args[2]
    code_length = int(args[3]) if len(args) > 3 else None
    maximum_guesses = int(args[4]) if len(args) > 4 else None
    available_colours = args[5:]
    

if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        print(f'Unexpected error occurred: {e}')
        sys.exit(6)
