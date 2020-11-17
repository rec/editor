"""
🖋 editor - open a text editor from inside Python 🖋
------------------------------------------------------------------

`editor` opens a text editor for an existing file, a new file, or a tempfile,
blocks while the user edits text, then returns the results.

EXAMPLE
========

Using a temporary file
~~~~~~~~~~~~~~~~~~~~~~~~~

If no filename is provided, a temporary file gets edited, and its
contents returned.

.. code-block:: python

    import editor

    MESSAGE = 'Insert comments below this line\\n\\n'
    comments = editor(text=MESSAGE)
    # Pops up the default editor with a tempfile, containing MESSAGE

EXAMPLE
=========

Using a named file
~~~~~~~~~~~~~~~~~~~~

If a filename is provided, then it gets edited!

.. code-block:: python

    import os

    FILE = 'file.txt'
    assert not os.path.exists(FILE)

    comments = editor(text=MESSAGE, filename=FILE)
    # Pops up an editor for new FILE containing MESSAGE, user edits

    assert os.path.exists(FILE)

    # You can edit an existing file too, and select your own editor.
    # By default, it uses the editor from the environment variable EDITOR

    comments2 = editor(filename=FILE, editor='emacs')
"""

from pathlib import Path
import os
import platform
import runs
import tempfile
import traceback
import xmod

__all__ = 'editor', 'default_editor'
__version__ = '1.1.0'

DEFAULT_EDITOR = 'vim'
EDITORS = {'Windows': 'notepad'}


@xmod
def editor(text=None, filename=None, editor=None, **kwargs):
    """
    Open a text editor, block while the user edits, then return the results

    ARGUMENTS
      text
        A string which is written to the file before the editor is opened.
        If `None`, the file is left unchanged.

      filename
        The name of the file to edit.  If `None`, a temporary file is used.

      editor
        A string containing the command used to invoke the text editor.
        If `None`, use `editor.default_editor()`.

      kwargs
        Arguments passed on to `runs.call()`, an enhanced `subprocess.call()`
"""
    editor = editor or default_editor()
    is_temp = not filename
    if is_temp:
        fd, filename = tempfile.mkstemp()
        os.close(fd)

    try:
        path = Path(filename)
        if text is not None:
            path.write_text(text)

        cmd = '{} {}'.format(editor, filename)
        runs.call(cmd, **kwargs)
        return path.read_text()

    finally:
        if is_temp:
            try:
                filename.remove()
            except Exception:
                traceback.print_exc()


def default_editor():
    """
    Return the default text editor.

    The default text editor is the contents of the environment variable
    `EDITOR`, it it's non-empty, otherwise if the platform is Windows, it's
    `'notepad'`, otherwise `'vim'`.
    """
    return os.environ.get('EDITOR') or (
        EDITORS.get(platform.system(), DEFAULT_EDITOR)
    )
