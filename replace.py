#!/usr/bin/env python3

import re
import sys
import argparse

if sys.version_info[0] != 3:
    print("This script requires Python version > 3.0")
    sys.exit(1)

# The delimiter that separates the entries in the regex file
DELIMITER = "~"
FILE_ENCODING = "utf-8"


def replace_from_file(content_filename, replace_filename, output_filename, regex=False):
    """
    For every line in the replace_file, perform a replacement in the content_file
    The replace_file uses the delimiter |, simply escape the delimiter (\|) if
    you want to replace that character The last delimited string on a line is the
    replace word for that replace_list.

    For example, if one line of the replace file is
        1|2|3|4|9
    then all instances of 1, 2, 3, or 4 will be replaced with 9 in the content file.

    :param Union[list, str] content_filename:    Name of the file that is having content replaced
    :param str              replace_filename:    Definitions of the replace mappings
    :param str              output_filename:     Name of the file with replaced contents
    :param bool             regex:               Whether to use regex searching or not
    """
    # If content_filename is a single string, put it into a one-element list
    iterator = (content_filename,) if not isinstance(content_filename, (tuple, list)) else content_filename

    if len(iterator) > 1:
        raise TypeError("only supports one input file currently")

    for filename in iterator:
        content_file = open(filename, encoding = FILE_ENCODING)
        replace_file = open(replace_filename, "r+", encoding = FILE_ENCODING)

        contents = content_file.read()

        for line in replace_file.readlines():
            # Use negative lookbehind to not split on escaped delimiters
            temp = re.split(r'(?<!\\)' + re.escape(DELIMITER), line.rstrip("\n"))

            replace_list = temp[:-1]
            # Now that the list has been split, unescape the delimiter
            replace_list = [x.replace("\\" + DELIMITER, DELIMITER) for x in replace_list]

            replace_word = temp[-1]

            contents = replace_strings(contents, replace_list, replace_word, regex)

        new_file = open(output_filename, "w", encoding = FILE_ENCODING)
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
    :param bool             regex:          Whether to use regex searching or not
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Replaces contents of file based on predefined regex patterns.')
    parser.add_argument('-r', '--regex', action = 'store_true', help = 'Use regex matching')
    parser.add_argument('content_filename', metavar = 'input_file', nargs = '+', help = 'File to replace contents of')
    parser.add_argument('replace_filename', metavar = 'regex_file', help = 'File to get the regex patterns from')
    parser.add_argument('output_filename', metavar = 'output_file', default = 'replaced.txt', nargs = '?',
                        help = 'Name of the file with replaced contents (default: replaced.txt)')
    args = parser.parse_args()

    replace_from_file(**vars(args))
