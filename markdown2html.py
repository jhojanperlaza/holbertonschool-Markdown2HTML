#!/usr/bin/python3
"""Script that generate a README file
    -Start a script:
        *First argument is the name of the Markdown file
        *Second argument is the output file name
    -Parsing Headings Markdown syntax for generating HTML
    -Parsing Unordered listing syntax for generating HTML
"""
from sys import argv, stderr
import os


if __name__ == "__main__":

    def heading(line):
        heading_level = line.count('#')
        line = line.replace('#', '').replace('\n', '')
        str_return = "<h{}>{}</h{}>".format(heading_level, line, heading_level)
        return str_return

    def unordered_list(lines, expression):
        list_returnt = []
        for line in lines:
            line = line.replace('-', '').replace('*', '').replace('\n', '')
            list_returnt.append("\t<li>{}</li>\n".format(line))

        if expression == '-':
            str_return = "<ul>\n{}</ul>".format(''.join(list_returnt))
        else:
            str_return = "<ol>\n{}</ol>".format(''.join(list_returnt))

        return str_return

    def paragraph(lines):

        if len(lines) > 1:
            list_returnt = []
            for line in lines[:-1]:
                line = "\t" + line
                list_returnt.append(line.replace('\n', '\n\t<br />\n'))
            str_return = "<p>\n{}\t{}</p>".format(''.join(list_returnt), lines[-1])
        else:
            str_return = "<p>\n\t{}</p>".format(''.join(lines[0]))

        return str_return

    expressions = {"-": unordered_list, "#": heading, "*": unordered_list}

    if len(argv) <= 2:
        stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    name_file = argv[1]

    if not os.path.exists(name_file):
        stderr.write("Missing {}\n".format(name_file))
        exit(1)

    lines_to_write = []
    listing_lines = []
    text_lines = []
    previous_expression = ""
    with open(name_file, 'r') as f:
        file_lines = f.readlines()
        last = file_lines[-1]

        for line in file_lines:
            if line[0] in expressions:
                if line[0] == '-' or line[0] == '*':
                    previous_expression = line[0]
                    listing_lines.append(line)
                    if line is last and len(listing_lines) != 0:
                        new_line = expressions[line[0]](listing_lines, line[0])
                        lines_to_write.append(new_line)
                    continue
                if len(listing_lines) != 0:
                    new_line = expressions[previous_expression](
                        listing_lines, previous_expression)
                    lines_to_write.append(new_line)
                    listing_lines = []

                new_line = expressions[line[0]](line)
                lines_to_write.append(new_line)
            else:
                if line[0].isalpha() == False:
                    if len(text_lines) != 0:
                        new_line = paragraph(text_lines)
                        lines_to_write.append(new_line)
                        text_lines = []
                    continue
                if line[0].isalpha():
                    text_lines.append(line)
                    if line is last:
                        new_line = paragraph(text_lines)
                        lines_to_write.append(new_line)

    with open(argv[2], 'w') as f:
        for line in lines_to_write:
            f.write(line)
            f.write('\n')

    exit(0)
