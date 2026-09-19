import shlex
import unittest
from pathlib import Path
from unittest import mock

import tdir

import editor

FILENAME = 'a_file.txt'
EDITOR = editor.default_editor()
TEST_CONTENT = 'roses are red,\nwater is blue.\n'


@mock.patch('editor.subprocess.call', autospec=True)
class TestEditor(unittest.TestCase):
    @tdir(FILENAME)
    def test_existing(self, call):
        actual = editor(filename=FILENAME)
        expected = FILENAME + '\n'
        assert actual == expected

        filename = Path(FILENAME).resolve()
        call.assert_called_once_with([*shlex.split(EDITOR), str(filename)])

        actual = editor('X', filename=filename)
        expected = 'X'
        assert actual == expected

    @tdir
    def test_new(self, call):
        actual = editor('X', filename=FILENAME, shell=True)
        expected = 'X'
        assert actual == expected

        filename = Path(FILENAME).resolve()
        expected = [*shlex.split(EDITOR), str(filename)]
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

    @tdir
    def test_configured_encoding(self, call):
        Path(FILENAME).write_bytes(b'caf\xe9')

        actual = editor(filename=FILENAME, encoding='latin-1')

        assert actual == 'café'

    def test_temp_cleanup_keeps_editor_failure_visible(self, call):
        call.side_effect = RuntimeError('editor failed')

        with mock.patch.object(Path, 'unlink', side_effect=OSError('cleanup failed')):
            with self.assertRaisesRegex(RuntimeError, 'editor failed'):
                editor()

    def test_default_editor_prefers_visual_then_editor_then_platform(self, call):
        with mock.patch.dict('os.environ', {'VISUAL': 'visual', 'EDITOR': 'edit'}):
            assert editor.default_editor() == 'visual'
        with mock.patch.dict('os.environ', {'EDITOR': 'edit'}, clear=True):
            assert editor.default_editor() == 'edit'
        with mock.patch.dict('os.environ', {}, clear=True):
            with mock.patch('editor.platform.system', return_value='Windows'):
                assert editor.default_editor() == 'notepad'

    @tdir
    def test_sequence_editor_keeps_paths_as_one_argument(self, call):
        filename = 'a "quoted" file.txt'

        editor.editor(text='', filename=filename, editor=['emacs', '-nw'])

        call.assert_called_once_with(['emacs', '-nw', str(Path(filename).resolve())])


def main():
    print(editor.editor())


def test_main(monkeypatch, capsys):
    monkeypatch.setattr('editor.editor', lambda: TEST_CONTENT)

    main()

    assert TEST_CONTENT + '\n' == capsys.readouterr().out
