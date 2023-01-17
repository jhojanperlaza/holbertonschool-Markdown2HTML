#!/usr/bin/python3
"""Script that generate a README file
    -Start a script:
        *First argument is the name of the Markdown file
        *Second argument is the output file name
"""
from sys import argv, stderr
import os


if __name__ == "__main__":

    def heading(line):
        heading_level = line.count('#')
        line = line.replace('#', '').replace('\n', '').replace(' ', '')
        str_return = "<h{}>{}</h{}>".format(heading_level, line, heading_level)
        return str_return


    expressions = {"#":heading}

    if len(argv) <= 2:
        stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    name_file = argv[1]

    if not os.path.exists(name_file):
        stderr.write("Missing {}\n".format(name_file))
        exit(1)

    list_lines = []
    with open(name_file) as f:
        for line in f:
            if line[0] in expressions:
                new_line = expressions[line[0]](line)
                list_lines.append(new_line)



    with open(argv[2], 'w') as f:
        for line in list_lines:
            f.write(line)
            f.write('\n')

    exit(0)

