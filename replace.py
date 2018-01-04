#!/usr/bin/env python3

import re
import sys

if sys.version_info[0] != 3:
    print("This script requires Python version > 3.0")
    sys.exit(1)

# The delimiter that separates the entries in the regex file
REGEX_DELIMITER = "|"
FILE_ENCODING = "utf-8"


def replace_from_file(content_filename, replace_filename, regex=False):
    """
    For every line in the replace_file, perform a replacement in the content_file
    The replace_file uses the delimiter |, simply escape the delimiter (\|) if
    you want to replace that character The last delimited string on a line is the
    replace word for that replace_list.

    For example, if one line of the replace file is
        1|2|3|4|9
    then all instances of 1, 2, 3, or 4 will be replaced with 9 in the content file.

    :param str content_filename:    Name of the file that is having content replaced
    :param str replace_filename:    Definitions of the replace mappings
    :param bool           regex:    Whether to use regex searching or not
    """
    content_file = open(content_filename, encoding=FILE_ENCODING)
    replace_file = open(replace_filename, "r+", encoding=FILE_ENCODING)
    
    contents = content_file.read()

    for line in replace_file.readlines():
        # Use negative lookbehind to not split on escaped delimiters
        temp = re.split(r'(?<!\\)\|', line.rstrip("\n"))

        replace_list = temp[:-1]
        # Now that the list has been split, unescape the delimiter
        replace_list = [x.replace("\\|", "|") for x in replace_list]

        replace_word = temp[-1]

        contents = replace_strings(contents, replace_list, replace_word, regex)

    new_file = open("test.txt", "w", encoding=FILE_ENCODING)
    new_file.write(contents)

    content_file.close()
    replace_file.close()


def replace_strings(original, replace_list, replace_word, regex=False):
    """
    Takes a text where replacements are desired, and for each occurrence of a pattern
    in replace_list, replaces it with the given replace_word. Can be set to regex matching
    if desired.

    :param str              original:       The original text to replace words in
    :param Union[list, str] replace_list:   The list of words to replace
    :param str              replace_word:   The word to replace with
    :return str: The text with the specified characters replaced
    """
    if not isinstance(original, str):
        raise TypeError('parameter "original" must have type str')
    if not isinstance(replace_word, str):
        raise TypeError('parameter "replace_word" must have type str')

    # Escape any regex characters if script not being run in regex mode
    escaped = [x if regex else re.escape(x) for x in replace_list]
    reg = "(" + "|".join(escaped) + ")"

    return re.sub(reg, replace_word, original)


# replace_from_file("01-03-18 Messages.xml", "replace.txt")
