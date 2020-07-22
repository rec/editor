from pathlib import Path
import os
import subprocess
import tempfile
import xmod

EDITOR = os.environ.get('EDITOR', 'vim')
__version__ = '0.9.0'


@xmod
def editor(initial_contents='', filename=None, editor=EDITOR):
    if not filename:
        with tempfile.NamedTemporaryFile(mode='r+') as fp:
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
