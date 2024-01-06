from pathlib import Path
import unittest
from unittest import mock

import tdir

import editor

FILENAME = 'a_file.txt'
EDITOR = editor.default_editor()
TEST_CONTENT = 'roses are red,\nwater is blue.\n'


@mock.patch('editor.runs.call', autospec=True)
class TestEditor(unittest.TestCase):
    @tdir(FILENAME)
    def test_existing(self, call):
        actual = editor(filename=FILENAME)
        expected = FILENAME + '\n'
        assert actual == expected

        filename = Path(FILENAME).resolve()
        call.assert_called_once_with('{} "{}"'.format(EDITOR, filename))

        actual = editor('X', filename=filename)
        expected = 'X'
        assert actual == expected

    @tdir
    def test_new(self, call):
        actual = editor('X', filename=FILENAME, shell=True)
        expected = 'X'
        assert actual == expected

        filename = Path(FILENAME).resolve()
        expected = '{} "{}"'.format(EDITOR, filename)
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


def main():
    print(editor.editor())


def test_main(monkeypatch, capsys):
    monkeypatch.setattr('editor.editor', lambda: TEST_CONTENT)

    main()

    assert TEST_CONTENT + '\n' == capsys.readouterr().out
