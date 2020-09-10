import os


def empty_lines(text):
    text = os.linesep.join([s for s in text.splitlines() if s])
    text = text.replace('  ', '')
    return os.linesep.join([s for s in text.splitlines() if s])
