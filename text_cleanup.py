import os


def empty_lines(text):
    return os.linesep.join([s for s in text.splitlines() if s])
