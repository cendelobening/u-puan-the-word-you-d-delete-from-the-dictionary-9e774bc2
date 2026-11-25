"""The word to delete from the dictionary: Delete.

Why "Delete" wins. The joke is the word itself, and it lands the instant
you read it: deleting "delete" is the only deletion that deletes itself.
Once it is gone, the dictionary can never again describe what happened
to it - the entry, the act and the punchline are one and the same word.
No caption or defence is needed, and no other pick can steal the trick.

Why not "Moist"? It is the famous answer, which is exactly the problem:
it is the first word every entrant reaches for, so freshness - a stated
criterion - counts against it, and byte-identical entries share one rate.
"Delete" is fresh, instantly understood by any reader, and at 6 letters
it is also the smaller text if a tie ever comes down to size.

Why not corporate jargon ("Synergy", "Leverage") or a hated chore
("Meeting", "Monday", "Homework")? Those jokes are about disliking a
thing; this one is about the word eating itself. The humour comes from
the word's own meaning, its double role as both the deletion and the
deleted, and the gap it leaves in the language: a dictionary with no
word for removal.
"""

import os
import tempfile

WORD = "Delete"


def _validate(word):
    """Return the word's UTF-8 bytes, or raise if it is not one clean word.

    The sealed gate requires 1-77 characters of UTF-8 text, not only
    whitespace. We go stricter: a single alphabetic token, no whitespace,
    no punctuation, no newline, nothing attached.
    """
    if not isinstance(word, str) or not word:
        raise ValueError("word must be a non-empty string")
    if not (1 <= len(word) <= 77):
        raise ValueError("word must be 1-77 characters, got %d" % len(word))
    if word.split() != [word]:
        raise ValueError("word must be a single token with no whitespace")
    if not word.isalpha():
        raise ValueError("word must be letters only")
    data = word.encode("utf-8")
    if not data.strip():
        raise ValueError("word must not be only whitespace")
    return data


def main():
    data = _validate(WORD)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    # Write via a temp file in the output dir, then atomically replace.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    os.chmod(target, 0o644)

    # Read back and verify the bytes on disk are exactly the word.
    with open(target, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("verification failed: bytes on disk differ")


if __name__ == "__main__":
    main()
