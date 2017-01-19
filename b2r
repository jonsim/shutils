#!/usr/bin/env python
import sys, math

def minimal_float(f):
    sf = str(round(f, 2))
    if sf[-2:] == ".0":
        sf = sf[:-2]
    return sf

def usage():
    print "usage: b2r [-h] [number-of-bytes]"
    print ""
    print "Tiny program to convert a raw number of bytes (either decimal or"
    print "prefixed hex) into a human readable form."
    print ""
    print "positional arguments:"
    print "  number-of-bytes    Number of bytes to convert. May be ommitted to"
    print "                     consume from stdin"
    print ""
    print "optional arguments:"
    print "  -h, --help         Print this message and exit"
    sys.exit(1)


argc = len(sys.argv)
lines = []
if argc == 1 and not sys.stdin.isatty():
    for line in sys.stdin:
        lines.append(line)
elif argc == 2:
    arg = sys.argv[1]
    if arg == "-h" or arg == "-help" or arg == "--help":
        usage()
    lines.append(arg)
else:
    usage()

UNIT_LETTERS = {0 : 'B', 1 : 'K', 2 : 'M', 3 : 'G', 4 : 'T', 5 : 'P'}
for line in lines:
    try:
        v = float(int(line, 10))
    except ValueError:
        v = float(int(line, 16))
    b = 0
    while v > 1024:
        v /= 1024
        b += 1
    print "%s%c" % (minimal_float(v), UNIT_LETTERS[b])
