# shutils
Collection of my (mostly) sh utils. Where not possible to use sh, bash has been
used instead, but a preference for sh has been made where possible. There are a
few Python files to. All of these have been written with Python 2.7.

## Installation
TODO

## Documentation
### b2r
#### Usage
```
usage: b2r [-h] [number-of-bytes]

Tiny program to convert a raw number of bytes (either decimal or
prefixed hex) into a human readable form.

positional arguments:
  number-of-bytes    number of bytes to convert. May be ommitted to
                     consume from stdin

optional arguments:
  -h, --help         print this message and exit
```

#### Examples
```sh
$ ./b2r.py 1234567890
1.15G

$ echo 0x512 | python b2r.py
1.27K
```