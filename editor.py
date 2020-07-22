import os
import subprocess
import tempfile
import xmod

EDITOR = os.environ.get('EDITOR', 'vim')
__version__ = '0.9.0'


@xmod
def editor(initial_contents='', filename=None, editor=EDITOR):
    def edit(fp, filename):
        subprocess.call([editor, filename])
        fp.seek(0)
        return fp.read()

    if filename:
        assert not initial_contents
        with open(filename) as fp:
            return edit(fp, filename)

    with tempfile.NamedTemporaryFile() as fp:
        fp.write(initial_contents)
        fp.flush()
        return edit(fp, fp.name)
