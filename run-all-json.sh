#!/bin/bash

# Set the directory containing the files you want to process
input_directory="./json/"
# Set the path to the output file where you want to store the results
output_file="output.txt"

# Empty the output file before starting the script
echo "" > "$output_file"

# Iterate over all files in the input directory
for file in "$input_directory"/*.json; do
  # Get the filename without the path
  filename="$(basename -- "$file")"

  # Remove the .json extension from the filename
  filename_no_ext="${filename%.json}"

  # Run the Python script with the current filename and save the output and errors to a temporary file
  output=$(python __init__.py "$filename_no_ext" 2>&1)

  # If the exit status of the Python script is non-zero, an error occurred
  if [ $? -ne 0 ]; then
    # Save the filename and error message to the output file
    echo "Filename: $filename" >> "$output_file"
    # comment out the below line to just get a list of the files that have errors when run
    # echo "Error: $output" >> "$output_file"
    echo "" >> "$output_file"
  fi
done