"""
🖋 editor - open a text editor 🖋️
-------------------------------------
"""

from pathlib import Path
import os
import subprocess
import tempfile
import xmod

__all__ = 'edit', 'default_editor'
__version__ = '0.9.0'


@xmod
def edit(initial_contents='', filename=None, editor=None):
    editor = editor or default_editor()
    if not filename:
        with tempfile.NamedTemporaryFile(mode='r+', suffix='.txt') as fp:
            fp.write(initial_contents)
            fp.flush()

            subprocess.call([editor, fp.name])

            fp.seek(0)
            return fp.read()

    path = Path(filename)
    if initial_contents:
        if path.exists():
            raise ValueError('Will not overwrite existing file')
        path.write_text(initial_contents)

    subprocess.call([editor, filename])
    return path.read_text()


def default_editor():
    return os.environ.get('EDITOR', 'vim')
