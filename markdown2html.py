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
import hashlib


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
            str_return = "<p>\n{}\t{}</p>".format(
                ''.join(list_returnt), lines[-1])
        else:
            str_return = "<p>\n\t{}\n</p>".format(
                ''.join(lines[0].replace('\n', '')))

        return str_return

    def bold(line):
        if '__' in line and '**' in line:
            li = line.split('__')
            line = "{}<em>{}</em>{}".format(li[0], li[1], li[2])
            l = line.split('**')
            str_return = "{}<b>{}</b>{}".format(l[0], l[1], l[2])
        elif '__' in line and '**' not in line:
            l = line.split('__')
            str_return = "{}<em>{}</em>{}".format(l[0], l[1], l[2])
        else:
            l = line.split('**')
            str_return = "{}<b>{}</b>{}".format(l[0], l[1], l[2])
        return str_return

    def computeMD5hash(line):
        l = line.replace('[[', '.').replace(']]', '.')
        l = l.split('.')
        m = hashlib.md5()
        m.update(l[1].encode('utf-8'))
        str_return = l[0] + m.hexdigest() + l[2]
        return str_return

    def replace_c(line):
        l = line.replace('((', '.').replace('))', '.')
        l = l.split('.')
        stri = l[1].replace('c', '').replace('C', '')
        return l[0] + stri + l[2]

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

            if '**' in line or '__' in line:
                if line is last:
                    last = bold(line)
                line = bold(line)
            if '[[' in line:
                if line is last:
                    last = computeMD5hash(line)
                line = computeMD5hash(line)
            if '((' in line:
                if line is last:
                    last = replace_c(line)
                line = replace_c(line)
            if line[0] in expressions and line[1] != '_' and line[1] != '*':
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
                if len(listing_lines) != 0:
                    new_line = expressions[previous_expression](
                        listing_lines, previous_expression)
                    lines_to_write.append(new_line)
                    listing_lines = []
                if line[0].isalpha() == False:
                    if len(text_lines) != 0:
                        new_line = paragraph(text_lines)
                        lines_to_write.append(new_line)
                        text_lines = []
                if line[0].isalpha():
                    text_lines.append(line)
                    if line == last:
                        new_line = paragraph(text_lines)
                        lines_to_write.append(new_line)
                if '<b>' in line or '<em>' in line:
                    if len(text_lines) == 0:
                        text_lines.append(line)
                        n = paragraph(text_lines)
                        lines_to_write.append(n)

    with open(argv[2], 'w') as f:
        for line in lines_to_write:
            f.write(line)
            f.write('\n')

    exit(0)
