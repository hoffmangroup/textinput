#!/usr/bin/env python

"""textinput: streamlined version of stdlib fileinput

Typical use is:

    import textinput
    for line in textinput.lines():
        process(line)

This iterates over the lines of all files listed in sys.argv[1:],
defaulting to sys.stdin if the list is empty.  If a filename is '-' it
is also replaced by sys.stdin.  To specify an alternative list of
filenames, pass it as the argument to input().  A single file name is
also allowed.
"""

from __future__ import absolute_import
__version__ = "0.1.3"

from setuptools import find_packages, setup

doclines = __doc__.splitlines()
name, short_description = doclines[0].split(": ")
long_description = "\n".join(doclines[2:])

url = "http://noble.gs.washington.edu/~mmh1/software/%s/" % name.lower()
download_url = "%s%s-%s.tar.gz" % (url, name, __version__)

classifiers = ["License :: OSI Approved :: GNU General Public License (GPL)",
               "Natural Language :: English",
               "Programming Language :: Python"]

setup(name=name,
      version=__version__,
      description=short_description,
      author="Michael Hoffman",
      author_email="mmh1@uw.edu",
      url=url,
      download_url=download_url,
      license="GNU GPLv2",
      classifiers=classifiers,
      long_description = long_description,
      package_dir = {'': 'lib'},
      py_modules = ['tabdelim', 'textinput'],
      scripts = ['scripts/innerjoin',
                 'scripts/filter',
                 'scripts/nohead',
                 'scripts/mean',
                 'scripts/hidehead',
                 'scripts/intersect'],
      zip_safe=True
      )
