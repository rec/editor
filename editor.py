"""
🖋 editor - open a text editor, user edits, return results  🖋
------------------------------------------------------------------

``editor`` opens an editor onto an existing file, a new file, or a tempfile,
lets the user edit text, and returns the results.

EXAMPLE: using a temporary file

If no filename is provided, a temporary file gets edited, and its
contents returned.

.. code-block:: python

    import editor

    MESSAGE = 'Insert comments below this line\n\n'
    comments = editor(MESSAGE)
    # Pops up the default editor with a tempfile, containing MESSAGE

EXAMPLE: Using a named file

If a filename is provided, then it gets edited!

.. code-block:: python

    import os

    FILE = 'file.txt'
    assert not os.path.exists(FILE)

    comments = editor(MESSAGE, filename=FILE)
    # Pops up an editor for new FILE containing MESSAGE, user edits

    assert os.path.exists(FILE)

    # You can edit an existing file too, and select your own editor.
    # By default, it uses the editor from the environment variable EDITOR

    comments2 = editor(filename=FILE, editor='emacs')
"""

from pathlib import Path
import os
import subprocess
import tempfile
import xmod

__all__ = 'editor', 'default_editor'
__version__ = '0.9.0'


@xmod
def editor(initial_contents=None, filename=None, editor=None):
    """
    Open a text editor, user edits, return results

    ARGUMENTS
      initial_contents
        If not None, this string is written to the file before the editor
        is opened.

      filename
        If not None, the name of the file to edit.  If None, a temporary file
        is used.

      editor
        The path to an editor to call.  If None, use editor.default_editor()
    """
    editor = editor or default_editor()
    if not filename:
        with tempfile.NamedTemporaryFile(mode='r+', suffix='.txt') as fp:
            if initial_contents is not None:
                fp.write(initial_contents)
                fp.flush()

            subprocess.call([editor, fp.name])

            fp.seek(0)
            return fp.read()

    path = Path(filename)
    if initial_contents is not None:
        path.write_text(initial_contents)

    subprocess.call([editor, filename])
    return path.read_text()


def default_editor():
    """
    Return the default text editor.

    This is the contents of the environment variable EDITOR, or  ``'vim'`` if
    that variable is not set or is empty.
    """
    return os.environ.get('EDITOR', 'vim')
