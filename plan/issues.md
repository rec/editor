# editor issues and remediation plan

## Issues

1. **Editor command construction is shell-quoting dependent.** The command is
   built with an interpolated string and double quotes. Editor values or paths
   containing quotes are mishandled, and the behavior differs between POSIX
   shells and Windows command interpreters.
2. **The editor launch contract is under-specified.** It is unclear whether an
   editor string is a command, a shell fragment, or an executable plus
   arguments. This matters for `VISUAL`, `EDITOR`, paths containing spaces, and
   Windows.
3. **Text encoding is implicit.** Existing and temporary files are read and
   written with the platform default encoding, with no way to choose a codec or
   decoding error policy.
4. **Temporary-file cleanup hides all failures.** Catching `Exception` during
   unlink prints a traceback but allows the original operation to appear
   successful while leaving a file behind.
5. **Documentation has stale platform details.** It calls the Windows default
   `Notepad` while the implementation uses `notepad`, and repeats “the”.
6. **Typing does not describe the launch options.** The public `**kwargs: Any`
   obscures the forwarded call contract, and the function parameter named
   `editor` hides the module's principal function name in documentation.

## Remediation plan

1. Decide the accepted editor-command representation, then make command and
   path handling explicit and add tests for arguments and paths containing
   spaces and quotes on the supported platform.
2. Preserve the selected legacy form as needed, document the cross-platform
   rules, and test the default-editor precedence.
3. Add explicit, opt-in text decoding controls to the public API and cover
   UTF-8, configured decoding, and invalid bytes.
4. Narrow temporary-file cleanup handling to expected missing-file cases and
   ensure original editor failures remain visible.
5. Correct README and generated API documentation, including the exact default
   editor policy.
6. Refine public annotations where the underlying process API permits it
   without inventing a second launch interface.
