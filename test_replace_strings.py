import replace
from replace import REGEX_DELIMITER as RD
from unittest import TestCase

normal_string = "The 'quick' \"brown\" fox."
weird_string = "^^$*.?|]"
delimiter_string = "hi" + RD + " fun" + RD + " times" + RD


class TestReplace(TestCase):
    """
    Tests replacing in normal mode - no regex
    """

    def test_replace_nothing(self):
        """
        Test that the function returns an empty string if given empty strings
        """
        result = replace.replace_strings("", ["", ""], "")
        self.assertEqual("", result)
        print(replace.REGEX_DELIMITER)

    def test_replace_single_quote(self):
        result = replace.replace_strings(normal_string, "'", "1")
        self.assertEqual('The 1quick1 "brown" fox.', result)

    def test_replace_double_quote(self):
        result = replace.replace_strings(normal_string, '"', "")
        self.assertEqual("The 'quick' brown fox.", result)

    def test_replace_single_and_double_quote(self):
        result = replace.replace_strings(normal_string, ["'", '"'], "54")
        self.assertEqual("The 54quick54 54brown54 fox.", result)

    def test_replace_regex_chars(self):
        """
        Test replacing commonly used regex characters
        """
        result = replace.replace_strings(weird_string, ["^", "$", "*", ".", "?", "|", "]"], "2")
        self.assertEqual("22222222", result)

    def test_replace_delimiter(self):
        result = replace.replace_strings(delimiter_string, RD, "2")
        self.assertEqual("hi2 fun2 times2", result)


class TestReplaceRegex(TestCase):
    def test_replace_nothing(self):
        """
        Test that the function returns an empty string if given empty strings
        """
        result = replace.replace_strings("", ["", ""], "", True)
        self.assertEqual("", result)


class TestReplaceBadInput(TestCase):
    def test_bad_original_str(self):
        with self.assertRaises(TypeError):
            replace.replace_strings([""], "", "")

    def test_bad_replace_word(self):
        with self.assertRaises(TypeError):
            replace.replace_strings("", "", [""])

    def test_bad_filenames(self):
        with self.assertRaises(FileNotFoundError):
            replace.replace_from_file("fakefile.fff", "eee.444")
