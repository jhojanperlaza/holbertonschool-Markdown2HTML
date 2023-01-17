#!/usr/bin/python3
"""Script that generate a README file
    -Start a script:
        *First argument is the name of the Markdown file
        *Second argument is the output file name
"""
from sys import argv, stderr
import os
if __name__ == "__main__":
    if len(argv) <= 2:
        stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    elif not os.path.exists(argv[1]):
        stderr.write("Missing {}\n".format(argv[1]))
        exit(1)

    exit(0)
