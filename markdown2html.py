#!/usr/bin/python3
"""Script that generate a README file
    -Start a script:
        *First argument is the name of the Markdown file
        *Second argument is the output file name
"""
import sys
import os
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./markdown2html.py README.md README.html")
        exit(1)
        
    elif not os.path.isfile("./" + sys.argv[1]):
        print("Missing <filename>")
        exit(1)

    exit(0)
