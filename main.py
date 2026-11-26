"""The Comment Above the Code — make.fun entry.

Writes a single funny code comment to $MAKEFUN_OUTPUT_DIR/entry.txt:
the classic programmer's warning above a function that nobody dares
to touch, because nobody — not even its author — understands why it
works. Only the Python standard library is used.
"""

import os
import sys

CODE_COMMENT = "# This function works. I have no idea why. I have no idea how. Do not touch it, do not look at it, do not even think about it."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 200 characters. The req JSON agrees here,
# but the RULES.txt figure is the authority.
MAX_CHARS = 200


def validate_comment(text):
    """Return the comment once it passes the sealed gate, else raise.

    The gate counts UTF-8 characters, not bytes, so the line must be a
    single line of 1 to 200 characters, not only whitespace, with no
    trailing newline and no control characters in the output file.
    """
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, gate allows 1 to {MAX_CHARS}"
        )
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def describe_comment(text):
    """Summarise a comment the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so an ASCII comment
    reads the same either way while a comment with wide characters
    would not. Returns a one-line human-readable summary.
    """
    encoded = text.encode("utf-8")
    return (
        f"{len(text)} characters, {len(encoded)} UTF-8 bytes, "
        f"{len(text.split())} words"
    )


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    comment = validate_comment(CODE_COMMENT)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(comment)
    print(f"wrote {path} ({describe_comment(comment)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
