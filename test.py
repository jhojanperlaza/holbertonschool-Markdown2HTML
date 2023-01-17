#!/usr/bin/python3
"""
Test case
"""
import os
import random
import string
import time
from bs4 import BeautifulSoup


def random_string(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


fn_md = "{}.md".format(random_string())
fn_html = "{}.html".format(random_string())

# remove initial MD file
if os.path.exists(fn_md):
    os.remove(fn_md)

# remove initial HTML file
if os.path.exists(fn_html):
    os.remove(fn_html)

# create MD file
c = """
##### title
#### Hello title
# Holberton
## New title
### And with space
## Suspendisse in fringilla risus. Sed fermentum magna et nibh eleifend facilisis. Vestibulum euismod ultricies viverra. Integer leo tellus, maximus at luctus sed, rhoncus quis elit
##### dui id erat dignissim
# Top
###### School
"""
with open(fn_md, 'w') as f:
    f.write(c)

# run
os.system("./markdown2html.py {} {}".format(fn_md, fn_html))
time.sleep(1)


result = [
    {'name': "h5", 'value': "title"},
    {'name': "h4", 'value': "Hello title"},
    {'name': "h1", 'value': "Holberton"},
    {'name': "h2", 'value': "New title"},
    {'name': "h3", 'value': "And with space"},
    {'name': "h2", 'value': "Suspendisse in fringilla risus. Sed fermentum magna et nibh eleifend facilisis. Vestibulum euismod ultricies viverra. Integer leo tellus, maximus at luctus sed, rhoncus quis elit"},
    {'name': "h5", 'value': "dui id erat dignissim"},
    {'name': "h1", 'value': "Top"},
    {'name': "h6", 'value': "School"}
]

# parse HTML file
with open(fn_html, "r") as f:
    root = BeautifulSoup(f.read(), 'html.parser')
    all_tags = [tag for tag in root.find_all()]
    if len(all_tags) == 0:
        print("No tag found")
        exit(1)
    if len(all_tags) != len(result):
        print("Too many tags: {}".format(all_tag_names))
    for idx in range(0, len(all_tags)):
        tag = all_tags[idx]
        res_tag = result[0]

        if tag.name != res_tag['name']:
            print("Wrong tag: {} instead of {}".format(
                tag.name, res_tag['name']))
            exit(1)
        t_content = tag.string.strip()
        if t_content != res_tag['value']:
            print("Wrong tag content: {} instead of {}".format(
                t_content, res_tag['value']))
            exit(1)
        del result[0]

    if len(result) > 0:
        print("Some tags are not found: {}".format(result))
    print("OK", end="")

# delete files
if os.path.exists(fn_md):
    os.remove(fn_md)
if os.path.exists(fn_html):
    os.remove(fn_html)
