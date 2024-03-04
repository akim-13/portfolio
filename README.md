# Solving Sudoku Puzzles
## Assignment Preamble
Please ensure you carefully read all of the details and instructions on the assignment page, this section, and the rest of the notebook. If anything is unclear at any time please post on the forum or ask a tutor well in advance of the assignment deadline.

In addition to all of the instructions in the body of the assignment below, you must also follow the following technical instructions for all assignments in this unit. *Failure to do so may result in a grade of zero.*
* [At the bottom of the page](#Submission-Test) is some code which checks you meet the submission requirements. You **must** ensure that this runs correctly before submission.
* Do not modify or delete any of the cells that are marked as test cells, even if they appear to be empty.
* Do not duplicate any cells in the notebook – this can break the marking script. Instead, insert a new cell (e.g. from the menu) and copy across any contents as necessary.

Remember to save and backup your work regularly, and double-check you are submitting the correct version.

This notebook is the primary reference for your submission. You may write code in separate `.py` files but it must be clearly imported into the notebook so that it runs without needing to reference those files, and you must explain clearly what functionality is contained in those files (through comments, markdown cells, etc).

As always, **the work you submit for this assignment must be entirely your own.** Do not copy or work with other students. Do not copy answers that you find online. These assignments are designed to help improve your understanding first and foremost – the process of doing the assignment is part of *learning*. They are also used to assess your ability, and so you must uphold academic integrity. Submitting plagiarised work risks your entire place on your degree.

**The pass mark for this assignment is 40%.** We expect that students, on average, will be able to produce a submission which gets a mark between 50-70% within the normal workload allocation for the unit, but this will vary depending on individual backgrounds. Please ask for help if you are struggling.

## Getting Started
For this assignment, you will be writing an agent that can solve sudoku puzzles. You should be familiar with sudoku puzzles from the unit material. You are given a 9x9 grid with some fixed values. To solve the puzzle, the objective is to fill the empty cells of the grid such that the numbers 1 to 9 appear exactly once in each row, column, and 3x3 block of the grid. 

Below is a sample puzzle along with its solution. 

<img src="images/sudoku.png" style="width: 50%;"/>

For the this part of the assignment you will need to submit the implementation for an agent which can solve sudoku puzzles – this notebook:
 * You can use any algorithm you like, from the unit material or otherwise
 * Your code will be subject to automated testing, from which grades will be assigned based on whether it can solve sudokus of varying difficulty
 * To get a high grade on this assignment, the speed of your code will also be a factor – the quicker the better
 * There are some sample tests included below, make sure your code is compatible with the format of these tests

### Choice of Algorithm
The choice of algorithm to solve sudoku puzzles is up to you. We expect you will use search techniques from the unit, but you could make something up yourself, or do some independent research to find something else. You will need to evaluate and balance the trade-off between how well suited you think the algorithm is and how difficult it is to write, but there is some advice below.

I suggest you implement *constraint satisfaction* as it is described in the unit material. You can use the code you have previously been given as a guide. A good implementation of a backtracking depth-first search with constraint propagation should be sufficient to get a good grade in the automated tests (roughly 60-70%).

You could also write a successful agent that uses the other search techniques you have seen in the unit so far: basic search, heuristic search, or local search. You may find these easier to implement, though they may perform less well. 

To get a high grade on this assignment will require a particularly efficient implementation of constraint satisfaction, or something which goes beyond the material we have presented. *This is left unguided and is not factored into the unit workload estimates.*

If you choose to implement more than one algorithm, please feel free to include your code and write about it in part two (report), but only the code in this notebook will be used in the automated testing.

## Sample Sudoku Puzzles
To get started, the cell below will load in some sample sudoku puzzles for you so you can see the format. There are sudokus provided of multiple difficulties (easier sudokus typically start with more digits provided). The cell below only loads the easiest, but there is another test cell lower in the notebook which will run your code against all of the provided puzzles.

Each sudoku is a 9x9 NumPy array of integers, where zero represents an empty square. Each difficulty comes with 15 sudokus, so when you load the file, it is stored in a 15x9x9 array.


```python
import numpy as np

# Load sudokus
sudoku = np.load("data/very_easy_puzzle.npy")
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")

# Load solutions for demonstration
solutions = np.load("data/very_easy_solution.npy")
print()

# Print the first 9x9 sudoku...
print("First sudoku:")
print(sudoku[0], "\n")

# ...and its solution
print("Solution of first sudoku:")
print(solutions[0])
```

    very_easy_puzzle.npy has been loaded into the variable sudoku
    sudoku.shape: (15, 9, 9), sudoku[0].shape: (9, 9), sudoku.dtype: int8
    
    First sudoku:
    [[1 0 4 3 8 2 9 5 6]
     [2 0 5 4 6 7 1 3 8]
     [3 8 6 9 5 1 4 0 2]
     [4 6 1 5 2 3 8 9 7]
     [7 3 8 1 4 9 6 2 5]
     [9 5 2 8 7 6 3 1 4]
     [5 2 9 6 3 4 7 8 1]
     [6 0 7 2 9 8 5 4 3]
     [8 4 3 0 1 5 2 6 9]] 
    
    Solution of first sudoku:
    [[1 7 4 3 8 2 9 5 6]
     [2 9 5 4 6 7 1 3 8]
     [3 8 6 9 5 1 4 7 2]
     [4 6 1 5 2 3 8 9 7]
     [7 3 8 1 4 9 6 2 5]
     [9 5 2 8 7 6 3 1 4]
     [5 2 9 6 3 4 7 8 1]
     [6 1 7 2 9 8 5 4 3]
     [8 4 3 7 1 5 2 6 9]]


## Part One
You should write all of your code for solving sudokus below this cell.

You must include a function called `sudoku_solver(sudoku)` which takes one sudoku puzzle (a 9x9 NumPy array) as input, and returns the solved sudoku as another 9x9 NumPy array. This is the function which will be tested. 


```python
def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    
    ### YOUR CODE HERE
    pass
    
    #return solved_sudoku

def main():
    print('hi')
# YOUR CODE HERE
if __name__ == "__main__":
    main()


#raise NotImplementedError()


```

    hi


All of your code must go above this cell. You may add additional cells into the notebook if you wish, but do not duplicate or copy/paste cells as this can interfere with the grading script.

### Testing Details
There are four difficulties of sudoku provided: very easy, easy, medium, and hard. There are 15 sample sudokus in each category, with solutions as well. Difficulty was determined using reference solvers, but your code may vary; it is conceivable that your code will find some sudokus much easier or harder within a given category, or even between categories.

*All categories that are easy and above will contain* ***invalid initial states***, that is, sudoku puzzles with no solution. In this case, your function should return a 9x9 NumPy array whose values are all equal to -1.

When we test your code, we will firstly test it on the *same* very easy puzzles that you have been given. Then we will test it on additional *hidden* sudokus from each difficulty in turn, easy and up. Grades are awarded based on whether your code can solve the puzzles. For high grades on the hard puzzles, execution time will also be a factor. 

All puzzles must take under 30 seconds each on the test machine to count as successful, but you should be aiming for an average of under a second per puzzle. Hardware varies, but all tests will take place on the same modern desktop machine. Our ‘standard constraint satisfaction’ implementation takes about 0.001 seconds per puzzle for the very easy category, but struggles to solve some of the hard puzzles within the time limit.

***The hard sudokus are labelled as hard for a reason.*** We expect most submissions will not be able to solve them in a reasonable length of time. Use the stop button (■) on the toolbar if you need to terminate your code because it is taking too long.

The best way to improve the performance of your code is through a detailed understanding and smart choice of AI algorithms. This assignment is ***not*** meant to test your ability to write multi-threaded code or any other kind of high-performance code optimisations. 

#### Test Cell
The following code will run your solution over the provided sudoku puzzles. To enable it, set the constant `SKIP_TESTS` to `False`. If you fail any tests of one difficulty, the code will stop, but you can modify this behaviour if you like.

**IMPORTANT**: you must set `SKIP_TESTS` back to `True` before submitting this file!


```python
SKIP_TESTS = True

if not SKIP_TESTS:
    import time
    import numpy as np
    __SCORES = {}
    difficulties = ['very_easy', 'easy', 'medium', 'hard']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")
        
        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")
        
        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)
            
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()
            
            if not isinstance(your_solution, np.ndarray):
                print("\033[91m[ERROR] Your sudoku_solver function returned a variable that has the incorrect type. If you submit this it will likely fail the auto-marking procedure result in a mark of 0 as it is expecting the function to return a numpy array with a shape (9,9).\n\t\033[94mYour function returns a {} object when {} was expected.\n\x1b[m".format(type(your_solution), np.ndarray))
            elif not np.all(your_solution.shape == (9, 9)):
                print("\033[91m[ERROR] Your sudoku_solver function returned an array that has the incorrect shape.  If you submit this it will likely fail the auto-marking procedure result in a mark of 0 as it is expecting the function to return a numpy array with a shape (9,9).\n\t\033[94mYour function returns an array with shape {} when {} was expected.\n\x1b[m".format(your_solution.shape, (9, 9)))
            
            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)
            
            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])
            
            print("This sudoku took {} seconds to solve.\n".format(end_time-start_time))

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        __SCORES[difficulty] = {
            'correct': count,
            'total': len(sudokus)
        }
```

## Submission Test
The following cell tests if your notebook is ready for submission. **You must not skip this step!**

Restart the kernel and run the entire notebook (Kernel → Restart & Run All). Now look at the output of the cell below. 

*If there is no output, then your submission is not ready.* Either your code is still running (did you forget to skip tests?) or it caused an error.

As previously mentioned, failing to follow these instructions can result in a grade of zero.


```python
import sys
import pathlib

fail = False;

success = '\033[1;32m[✓]\033[0m'
issue = '\033[1;33m[!]'
error = '\033[1;31m\t✗'
indent_success = '\033[1;32m\t✓'

#######
##
## Skip Tests check.
##
## Test to ensure the SKIP_TESTS variable is set to True to prevent it slowing down the automarker.
##
#######

if not SKIP_TESTS:
    fail = True;
    print("{} \'SKIP_TESTS\' is incorrectly set to False.\033[0m".format(issue))
    print("{} You must set the SKIP_TESTS constant to True in the cell above.\033[0m".format(error))
else:
    print('{} \'SKIP_TESTS\' is set to true.\033[0m'.format(success))

#######
##
## Report File Check.
##
## Test that checks there is a report pdf file found in the same folder as the notebook. This is required by the coursework specification.
##
#######

p1 = pathlib.Path('./report.pdf')
p2 = pathlib.Path('./Report.pdf')
if not (p1.is_file() or p2.is_file()):
    fail = True;
    print("{} Report PDF not found.\033[0m".format(issue))
    print("{} You must include a separate file called report.pdf in your submission.\033[0m".format(error))
else:
    print('{} Report PDF found.\033[0m'.format(success))

#######
##
## File Name check.
##
## Test to ensure file has the correct name. This is important for the marking system to correctly process the submission.
##
#######
    
p3 = pathlib.Path('./sudoku.ipynb')
if not p3.is_file():
    fail = True
    print("{} The notebook name is incorrect.\033[0m".format(issue))
    print("{} This notebook file must be named sudoku.ipynb\033[0m".format(error))
else:
    print('{} The notebook name is correct.\033[0m'.format(success))

#######
##
## Create classifier function check.
##
## Test that checks the create_classifier function exists. The function should train the classifier and return it so that it can be evaluated by the marking system.
##
#######

if "sudoku_solver" not in dir():
    fail = True;
    print("{} The sudoku_solver function has not been defined.\033[0m".format(issue))
    print("{} Your code must include a sudoku_solver function as described in the coursework specification.\033[0m".format(error))
    print("{} If you believe you have, \'restart & run-all\' to clear this error.\033[0m".format(error))
else:
    print('{} The sudoku_solver function has been defined.\033[0m'.format(success))



try:
    _sudoku = np.load("data/very_easy_puzzle.npy")[0]
    _solution = np.load("data/very_easy_solution.npy")[0]

    if not np.array_equal(sudoku_solver(_sudoku), _solution):
        print("{} Your sudoku_solver function does not correctly solve the first sudoku.\033[0m".format(issue))
        print()
        print("{} Your assignment is unlikely to get any marks from the autograder. While we will\033[0m".format(error))
        print("{} try to check it manually to assign some partial credit, we encourage you to ask\033[0m".format(error))
        print("{} for help on the forum or directly to a tutor.\033[0m".format(error))
        print()
        print("{} Please use the report file to explain your code anyway.\033[0m".format(error))
    else:
        print("{} Your sudoku_solver function correctly solves the first sudoku.\033[0m".format(success))
        if "__SCORES" in dir():
#             print("{} Test set summary - Not Found.\033[0m".format(issue))
#             print("{} Test set summary could not be found. This is automatically generated when the \033[0m".format(error))
#             print("{} above test cell is run. If you would like to see the summary please run the above cell.\033[0m".format(error))
#             print("{} You do not need this for submission, it is only for your convenience.\033[0m".format(error))
#         else:
            correct = 0
            total = 0
            for key, value in __SCORES.items():
                correct += value['correct']
                total += value['total']
                
            print("{} Test set summary - {}/{} Correct.\033[0m".format(issue, correct, total))
            if total != correct:
                
                for key, value in __SCORES.items():
                    if value['correct'] == value['total']:
                        print("{} {}/{} of {} sudokus correct.\033[0m".format(indent_success, value['correct'], value['total'], key))
                    else:
                        print("{} {}/{} of {} sudokus correct.\033[0m".format(error, value['correct'], value['total'], key))
            
except Exception as e:
    fail = True
    print("{} Error running test set.\033[0m".format(issue))
    print("{} Your code produced the following error. This error will result in a zero from the automarker, please fix.\033[0m".format(error))
    print(e)

    

#######
##
## Final Summary
##
## Prints the final results of the submission tests.
##
#######

if fail:
    sys.stderr.write("Your submission is not ready! Please read and follow the instructions above.")
else:
    print("\033[1m\n\n")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║                        Congratulations!                       ║")
    print("║                                                               ║")
    print("║            Your work meets all the required criteria          ║")
    print("║                   and is ready for submission.                ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print("\033[0m")
    
```


```python
# This is a TEST CELL. Do not delete or change.
```
