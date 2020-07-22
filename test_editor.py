from unittest import mock
import editor
import tdir
import unittest

FILENAME = 'a_file.txt'


@mock.patch('editor.subprocess.call', autospec=True)
class TestEditor(unittest.TestCase):
    @tdir(FILENAME)
    def test_existing(self, call):
        with self.assertRaises(ValueError) as m:
            editor('X', filename=FILENAME)
        assert m.exception.args[0] == 'Will not overwrite existing file'

        actual = editor(filename=FILENAME)
        expected = FILENAME + '\n'
        assert actual == expected

        call.assert_called_once_with([editor.EDITOR, FILENAME])

    @tdir
    def test_new(self, call):
        actual = editor('X', filename=FILENAME)
        expected = 'X'
        assert actual == expected

        call.assert_called_once_with([editor.EDITOR, FILENAME])

    def test_temp(self, call):
        actual = editor()
        expected = ''
        assert actual == expected
        call.assert_called_once()

    def test_temp2(self, call):
        actual = editor('some contents')
        expected = 'some contents'
        assert actual == expected
        call.assert_called_once()
