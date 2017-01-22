# (c) Copyright 2017 Jonathan Simmonds
"""Module providing very basic console utility functions."""
import fcntl
import termios
import struct

def console_size():
    """Derives the current console's size.

    NB: Taken from http://stackoverflow.com/a/3010495

    Returns:
        (width, height) of the current console.
    """
    try:
        h, w, hp, wp = struct.unpack('HHHH',
                                     fcntl.ioctl(1, termios.TIOCGWINSZ,
                                                 struct.pack('HHHH', 0, 0, 0, 0)))
    except IOError:
        w, h = (80, 40)
    return w, h
