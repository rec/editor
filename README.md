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

    comments = editor.editor(text='Comments here\n\n')
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

### Command and text handling

An editor command string retains its legacy POSIX `shlex` parsing. For portable
paths and editor arguments, pass an argv sequence instead:

    comments = editor.editor(filename=FILE, editor=['emacs', '-nw'])

The edited path is always one final argument, including when it contains spaces
or quotes. `encoding` and `errors` are optional controls for reading and
writing text; omit them to retain the platform-default behavior.

### [API Documentation](https://rec.github.io/editor#editor--api-documentation)

### A note on AI use

Version 2.0 has exactly the same API as before, and the great majority of the code is
still the handwritten code from before, but I recently used a coding assistant to find a
lot of possible errors and edge cases and fix them.

I believe it should do exactly what it did before, but not fail in some unusual but
certainly not impossible cases. Please let me know with an [issue
report](https://github.com/rec/editor/issues/new) if any problems crop up.
