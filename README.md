# 🖋 editor - Open the default text editor 🖋

`editor` opens a text editor for an existing file, a new file, or a tempfile,
blocks while the user edits text, then returns the results.

You can specify a command line that runs the editor, but usually you leave it
empty - in that case, `editor` uses the  the command line from the environment
variable `VISUAL`, or if that's empty, the environment variable `EDITOR`, or if
*that's* empty, either `Notepad` on Windows or `vi` elsewhere.

### Example 1: Using a temporary file

If no filename is provided, a temporary file gets edited, and its contents
returned.


    import editor

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
    comments2 = editor(filename=FILE, editor='emacs')


### [API Documentation](https://rec.github.io/editor#editor--api-documentation)
