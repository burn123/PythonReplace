import re

# The delimiter that separates the entries in the regex file
REGEX_DELIMITER = "|"


def replace_from_file(content_filename, replace_filename):
    """
    :param str content_filename:    Name of the file that is having content replaced
    :param str replace_filename:    Definitions of the replace mappings
    """
    content_file = open(content_filename, encoding="utf-8")
    replace_file = open(replace_filename, "r+", encoding="utf-8")
    
    contents = content_file.read()

    for line in replace_file.readlines():
        # Use negative lookbehind to not split on escaped delimiters
        temp = re.split(r'(?<!\\)\|', line.rstrip("\n"))

        replace_list = temp[:-1]
        # Now that the list has been split, unescape the delimiter
        replace_list = [x.replace("\\|", "|") for x in replace_list]

        replace_word = temp[-1]

        contents = replace_strings(contents, replace_list, replace_word)

    print(contents)

    content_file.close()
    replace_file.close()


def replace_strings(original, replace_list, replace_word, regex=False):
    """
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


# replace_from_file("01-03-18 Messages.xml", "replace.txt")
