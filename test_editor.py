import unittest
from unittest import mock

import tdir

import editor

FILENAME = 'a_file.txt'
EDITOR = editor.default_editor()


@mock.patch('editor.runs.call', autospec=True)
class TestEditor(unittest.TestCase):
    @tdir(FILENAME)
    def test_existing(self, call):
        actual = editor(filename=FILENAME)
        expected = FILENAME + '\n'
        assert actual == expected

        call.assert_called_once_with('{} {}'.format(EDITOR, FILENAME))

        actual = editor('X', filename=FILENAME)
        expected = 'X'
        assert actual == expected

    @tdir
    def test_new(self, call):
        actual = editor('X', filename=FILENAME, shell=True)
        expected = 'X'
        assert actual == expected

        expected = '{} {}'.format(EDITOR, FILENAME)
        call.assert_called_once_with(expected, shell=True)

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
