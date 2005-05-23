#!/usr/bin/env python
from __future__ import division

__version__ = "$Revision: 1.1.1.1 $"

"""
fastfileinput: streamlined version of stdlib fileinput

Typical use is:

    import fileinput
    for line in fileinput.input():
        process(line)

This iterates over the lines of all files listed in sys.argv[1:],
defaulting to sys.stdin if the list is empty.  If a filename is '-' it
is also replaced by sys.stdin.  To specify an alternative list of
filenames, pass it as the argument to input().  A single file name is
also allowed.

Many auxiliary functions of fileinput are not supported.

"files" changed to "filenames"
"""

import sys

_state = None

class FileInput(object):
    """class FileInput(filenames)
    """
    def __init__(self, filenames=None):
        # filenames must be an iterable
        # no longer support anything else
        
        if filenames is None:
            filenames = sys.argv[1:]
        if not filenames:
            filenames = ['-']

        self.filenames = filenames

    def __iter__(self):
        for filename in self.filenames:
            for line in fileopen(filename):
                yield line

def input(*args, **kwargs):
    global _state
    if _state:
        raise RuntimeError, "input() already active"
    _state = FileInput(*args, **kwargs)
    return _state

def fileopen(filename, *args, **kwargs):
    """Works like built-in open() except returns sys.stdin for -"""
    if filename == "-":
        if args:
            raise ValueError, "can't specify args with filename '-'"
        if kwargs:
            raise ValueError, "can't specify kwargs with filename '-'"
        return sys.stdin
    
    return open(filename, *args, **kwargs)

def main(args):
    pass

def _test(*args, **kwargs):
    import doctest
    doctest.testmod(sys.modules[__name__], *args, **kwargs)

if __name__ == "__main__":
    if __debug__:
        _test()
    sys.exit(main(sys.argv[1:]))
