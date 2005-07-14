#!/usr/bin/env python
from __future__ import division

__version__ = "$Revision: 1.1 $"

import csv
import sys

import textinput
import tools2

def _update_not_None(src, dest, *args):
    for key in args:
        val = src[key]
        if val is not None:
            dest[key] = val

    return dest

class _UnixTabDialect(csv.excel_tab):
    """
    just like excel-tab, but line terminator is "\n" not "\r\n"
    """
    lineterminator = "\n"
csv.register_dialect("unix-tab", _UnixTabDialect)

#### both list and dict

class _ReaderWriter(object):
    def __init__(self, *args, **keywds):
        self._started = False
        self.set_reader(*args, **keywds)
        self.set_writer()

    def set_reader(self, *args, **keywds):
        if self._started:
            raise RuntimeError, "iteration already started"
        
        self._reader_args = args
        self._reader_keywds = keywds

    def set_writer(self, *args, **keywds):
        if self._started:
            raise RuntimeError, "iteration already started"
        
        self._writer_args = args
        self._writer_keywds = keywds

    def __iter__(self):
        if self._started:
            raise RuntimeError, "iteration already started"

        self._started = True
        
        reader = self._reader_factory(*self._reader_args,
                                      **self._reader_keywds)
        writer = reader.writer(*self._writer_args, **self._writer_keywds)

        for row in reader:
            yield row
            writer.writerow(row)

def io(readerwriter_factory, filenames=None, inplace=None, backup=None,
       *args, **keywds):
    input_keywds = _update_not_None(locals(), {},
                                    "filenames", "inplace", "backup")

    f = textinput.lines(**input_keywds)
    return readerwriter_factory(f, *args, **keywds)

#### list versions

class ListReader(tools2.Surrogate):
    def __init__(self, csvfile, dialect=None, *args, **keywds):
        self.dialect = dialect

        if dialect is None:
            dialect = "excel-tab"

        data = csv.reader(csvfile, dialect, *args, **keywds)
        tools2.Surrogate.__init__(self, data)

    def __iter__(self):
        return iter(self._data)

    def writer(self, csvfile=sys.stdout, dialect=None, *args, **keywds):
        if dialect is None:
            dialect = self.dialect

        if dialect is None:
            dialect = "unix-tab"

        return ListWriter(csvfile, dialect, *args, **keywds)

class ListWriter(tools2.Surrogate):
    def __init__(self, csvfile=sys.stdout, dialect="unix-tab", *args, **keywds):
        data = csv.writer(csvfile, dialect, *args, **keywds)
        tools2.Surrogate.__init__(self, data)

class ListReaderWriter(_ReaderWriter):
    _reader_factory = ListReader

listio = tools2.partial(io, ListReaderWriter)
listinput = tools2.partial(io, ListReader)

#### dict versions

class DictReader(csv.DictReader):
    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect=None, *args, **keywds):
        self.dialect = dialect

        if dialect is None:
            dialect = "excel-tab"

        if fieldnames is None:
            self.header = True
            fieldnames = csv.reader(f, dialect, *args, **keywds).next()
        else:
            self.header = False

        csv.DictReader.__init__(self, f, fieldnames, restkey, restval, dialect,
                                *args, **keywds)

    def writer(self, f=sys.stdout, fieldnames=None, restval=None,
               extrasaction="raise", dialect=None, header=None,
               prepend=[], append=[], *args, **keywds):
        if fieldnames is None:
            fieldnames = self.fieldnames

        fieldnames = prepend + fieldnames + append

        if restval is None:
            restval = self.restval
            if restval is None:
                restval = ""

        if dialect is None:
            dialect = self.dialect

        if dialect is None:
            dialect = "unix-tab"

        if header is None:
            header = self.header

        return DictWriter(f, fieldnames, restval, extrasaction,
                          dialect, header, *args, **keywds)

class DictWriter(csv.DictWriter):
    def __init__(self, f, fieldnames, restval="", extrasaction="raise",
                 dialect="unix-tab", header=True, *args, **keywds):
        csv.DictWriter.__init__(self, f, fieldnames, restval, extrasaction,
                                dialect, *args, **keywds)
        
        if header:
            self.writeheader()
                 
    def writeheader(self):
        self.writerow(dict((fieldname, fieldname)
                           for fieldname in self.fieldnames))

class DictReaderWriter(_ReaderWriter):
    _reader_factory = DictReader
    
    def __init__(self, f=None, fieldnames=None, restkey=None, restval=None,
                 extrasaction=None, dialect=None, header=None, prepend=None,
                 append=None, *args, **keywds):
        super(DictReaderWriter, self).__init__(*args, **keywds)

        _update_not_None(locals(), self._reader_keywds,
                         "f", "fieldnames", "restkey", "restval", "dialect")
        _update_not_None(locals(), self._writer_keywds,
                         "extrasaction", "header", "prepend", "append")

dictio = tools2.partial(io, DictReaderWriter)
dictinput = tools2.partial(io, DictReader)

def dictoutput(f=sys.stdout, *args, **keywds):
    """
    can create as many as necessary
    """
    return DictWriter(f, *args, **keywds)

#### __main__

def main(args):
    pass

def _test(*args, **keywds):
    import doctest
    doctest.testmod(sys.modules[__name__], *args, **keywds)

if __name__ == "__main__":
    if __debug__:
        _test()
    sys.exit(main(sys.argv[1:]))
