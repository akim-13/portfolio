#!/bin/bash

# Define the path to the directory with examples.
examples_io_dir="examples_io"

# Read each line from calls.txt and execute the command.
while IFS= read -r line; do
    # Skip empty lines and lines that don't start with 'python Mastermind.py'.
    if [[ -z "$line" || ! $line == "python Mastermind.py"* ]]; then
        continue
    fi

    # Extract the input and output file names from the line.
    input_file=$(echo "$line" | awk '{print $3}')
    output_file=$(echo "$line" | awk '{print $4}')

    # Construct the full paths for the input and output files.
    full_input_path="${examples_io_dir}/${input_file}"
    full_output_path="${examples_io_dir}/${output_file}"

    # Construct the command.
    command=$(echo "$line" | sed "s|$input_file|$full_input_path|; s|$output_file|output.txt|")

    echo "\$ $command"
    eval "$command"
    echo "Exit code: $?"
    echo

    echo "\$ diff output.txt $full_output_path"
    diff output.txt "$full_output_path"

    echo
    echo "--------------------------------------------------"
    echo
done < "${examples_io_dir}/calls.txt"
