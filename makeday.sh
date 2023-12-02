#!/bin/bash

# Generate for a user input X the following file structure:
# Day X
# ├── dayX.py
# ├── sample_input.py
# └── input.txt

DIR="Day $1"

mkdir "$DIR"
touch "$DIR/sample_input.txt"
touch "$DIR/input.txt"
touch "$DIR/day$1.py"
