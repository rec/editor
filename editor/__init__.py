"""
# 🖋 editor - Open a text editor 🖋

`editor` opens the default text editor or your favorite editor to edit an existing file,
a new file, or a tempfile, blocks while the user edits text, then returns the contents
of the file.

You can pass a parameter `editor=` to specify an editor or leave it empty, in which
case the editor is:

* The contents of the environment variable `VISUAL`, if it's set, otherwise:
* The contents of the environment variable `EDITOR`, if it's set, otherwise:
* The string `'notepad'`, if the code is running on Windows, otherwise:
* The string `'vim'`

### Example 1: Using a temporary file

If no filename is provided, a temporary file gets edited, and its contents
returned.

    import editor

    comments = editor.editor(text='Comments here\\n\\n')
    # Pop up the default editor with a tempfile containing "Comments here",
    # then return the contents and delete the tempfile.

### Example 2: Using a named file

If a filename is provided, then that file gets edited.

    import os

    FILE = 'file.txt'
    assert not os.path.exists(FILE)

    comments = editor.editor(text=MESSAGE, filename=FILE)
    # Pop up an editor for a new FILE containing MESSAGE, user edits
    # This file is saved when the user exits the editor.

    assert os.path.exists(FILE)

    # You can edit an existing file too, and select your own editor.
    comments2 = editor.editor(filename=FILE, editor='emacs -nw')
"""

import os
import platform
import shlex
import subprocess
import tempfile
import traceback
import typing as t
from pathlib import Path

import xmod

__all__ = 'EditorCommand', 'editor', 'default_editor'

DEFAULT_EDITOR = 'vim'
EDITORS = {'Windows': 'notepad'}
EditorCommand: t.TypeAlias = str | t.Sequence[str]


@xmod.xmod(mutable=True)
def editor(
    text: t.Optional[str] = None,
    filename: Path | str | None = None,
    editor: EditorCommand | None = None,
    encoding: str | None = None,
    errors: str | None = None,
    **kwargs: t.Any,
) -> str:
    """
    Open a text editor, block while the user edits, then return the results

    Args:

      text: A string which is written to the file before the editor is opened.
          If `None`, the file is left unchanged.

      filename: The name of the file to edit.
          If `None`, a temporary file is used.

      editor: A legacy POSIX-style command string or an argv sequence used to
          invoke the text editor. The edited path is passed as one final argv
          element. If `None`, use `editor.default_editor()`.

      encoding, errors: Optional text encoding and decoding error policy for
          the edited file. If omitted, retain the platform default behavior.

      kwargs: Arguments passed on to `subprocess.call()`"""
    editor = editor or default_editor()
    is_temp = not filename
    if filename is not None:
        fname = filename
    else:
        fd, fname = tempfile.mkstemp()
        os.close(fd)

    path = Path(fname)
    try:
        if text is not None:
            path.write_text(text, encoding=encoding, errors=errors)

        command = shlex.split(editor) if isinstance(editor, str) else list(editor)
        subprocess.call([*command, str(path.resolve())], **kwargs)
        result = path.read_text(encoding=encoding, errors=errors)
    except BaseException:
        if is_temp:
            try:
                path.unlink()
            except OSError:
                traceback.print_exc()
        raise
    else:
        if is_temp:
            path.unlink(missing_ok=True)
        return result


def default_editor() -> str:
    """
    Return the default text editor.

    The default text editor is the contents of the environment variable
    `EDITOR`, it it's non-empty, otherwise if the platform is Windows, it's
    `'notepad'`, otherwise `'vim'`.
    """
    return os.environ.get('VISUAL') or (
        os.environ.get('EDITOR') or EDITORS.get(platform.system(), DEFAULT_EDITOR)
    )
