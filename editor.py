"""
🖋 editor - open a text editor, user edits, return results  🖋
------------------------------------------------------------------

``editor`` opens an editor onto an existing file, a new file, or a tempfile,
lets the user edit text, and returns the results.

EXAMPLE
========

Using a temporary file
~~~~~~~~~~~~~~~~~~~~~~~~~

If no filename is provided, a temporary file gets edited, and its
contents returned.

.. code-block:: python

    import editor

    MESSAGE = 'Insert comments below this line\\n\\n'
    comments = editor(MESSAGE)
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

    comments = editor(MESSAGE, filename=FILE)
    # Pops up an editor for new FILE containing MESSAGE, user edits

    assert os.path.exists(FILE)

    # You can edit an existing file too, and select your own editor.
    # By default, it uses the editor from the environment variable EDITOR

    comments2 = editor(filename=FILE, editor='emacs')
"""

from pathlib import Path
import os
import platform
import shlex
import subprocess
import tempfile
import traceback
import warnings
import xmod

__all__ = 'editor', 'default_editor'
__version__ = '1.0.0'

DEFAULT_EDITOR = 'vim'
EDITORS = {'Windows': 'notepad'}


@xmod
def editor(
    text=None,
    filename=None,
    editor=None,
    shell=False,
    initial_contents=None,
):
    """
    Open a text editor, user edits, return results

    ARGUMENTS
      text
        If not None, this string is written to the file before the editor
        is opened.

      filename
        If not None, the name of the file to edit.  If None, a temporary file
        is used.

      editor
        The path to an editor to call.  If None, use editor.default_editor()
        If None, use editor.default_editor().

        ``editor`` can either be a string, or a list or tuple of strings.
        Depending on the setting of ``shell=``, it will be converted into the
        right type using shlex.split or ``shlex.join``.

      shell
        Passed to subprocess.call

      initial_contents
        Same as ``text``.
        For backwards compatibility.

    """
    if initial_contents is not None:
        warnings.warn('Deprecated: use text= instead', DeprecationWarning)
        text = initial_contents

    if filename:
        file_to_edit = filename
    else:
        fd, file_to_edit = tempfile.mkstemp()
        os.close(fd)

    try:
        editor = editor or default_editor()
        if shell:
            if not isinstance(editor, str):
                editor = shlex.join(editor)
            editor = '{} {}'.format(editor, file_to_edit)
        else:
            if isinstance(editor, str):
                editor = shlex.split(editor)
            editor = [*editor, file_to_edit]

        path = Path(file_to_edit)
        if text is not None:
            path.write_text(text)

        subprocess.call(editor, shell=shell)
        return path.read_text()

    finally:
        if not filename:
            try:
                file_to_edit.remove()
            except Exception:
                traceback.print_exc()


def default_editor():
    """
    Return the default text editor.

    The default text editor is the contents of the environment variable EDITOR,
    it it's non-empty, otherwise if the platform is Windows, it's 'notepad',
    otherwise 'vim'.
    """
    return os.environ.get('EDITOR') or (
        EDITORS.get(platform.system(), DEFAULT_EDITOR))
