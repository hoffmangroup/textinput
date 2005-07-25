#!/usr/bin/env python

"""textinput: streamlined version of stdlib fileinput

Typical use is:

    import textinput
    for line in fileinput.lines():
        process(line)

This iterates over the lines of all files listed in sys.argv[1:],
defaulting to sys.stdin if the list is empty.  If a filename is '-' it
is also replaced by sys.stdin.  To specify an alternative list of
filenames, pass it as the argument to input().  A single file name is
also allowed.
"""

__version__ = "0.1.0"

from distutils.core import setup

doclines = __doc__.splitlines()
name, short_description = doclines[0].split(": ")
long_description = "\n".join(doclines[2:])

setup(name=name,
      version=__version__,
      description=short_description,
      author="Michael Hoffman",
      author_email="hoffman@ebi.ac.uk",
      url="http://www.ebi.ac.uk/~hoffman/software/",
      license="GNU GPL",
      long_description = long_description,
      package_dir = {'': 'lib'},
      py_modules = ['tabdelim', 'textinput'],
      scripts = ['scripts/innerjoin',
                 'scripts/filter',
                 'scripts/textsum'],
      )
