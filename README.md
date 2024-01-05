# 🖋 editor - Open a text editor 🖋

`editor` opens the default text editor or your favorite editor to edit an existing file,
a new file, or a tempfile, blocks while the user edits text, then returns the contents
of the file.

You can pass a parameter `editor=` to specify an editor or leave it empty, in which
case the editor is:

* The contents of the environment variable `VISUAL`, if it's set, otherwise:
* The the contents of the environment variable `EDITOR`, if it's set, otherwise:
* The string `'Notepad'`, if the code is running on Windows, otherwise:
* The string `'vim'`

### Example 1: Using a temporary file

If no filename is provided, a temporary file gets edited, and its contents
returned.

    from editor import editor

    MESSAGE = 'Insert comments below this line\n\n'
    comments = editor(text=MESSAGE)
    # Pops up the default editor with a tempfile, containing MESSAGE

### Example 2: Using a named file

If a filename is provided, then it gets edited!

    import os

    FILE = 'file.txt'
    assert not os.path.exists(FILE)

    comments = editor(text=MESSAGE, filename=FILE)
    # Pops up an editor for new FILE containing MESSAGE, user edits

    assert os.path.exists(FILE)

    # You can edit an existing file too, and select your own editor.
    comments2 = editor(filename=FILE, editor='emacs -nw')

### [API Documentation](https://rec.github.io/editor#editor--api-documentation)
