# shutils
Collection of my (mostly) sh utils. Where not possible to use sh, bash has been
used instead, but a preference for sh has been made where possible. There are a
few Python files to. All of these have been written with Python 2.7.

&copy; Copyright 2017 Jonathan Simmonds

## Installation
TODO

## Documentation
### b2r
#### Type
Python script

#### Usage
```
usage: b2r [-h] [number-of-bytes]

Tiny program to convert a raw number of bytes (either decimal or
prefixed hex) into a human readable form.

positional arguments:
  number-of-bytes    Number of bytes to convert. May be ommitted to
                     read from stdin

optional arguments:
  -h, --help         Print this message and exit
```

#### Examples
```sh
b2r 1234567890
1.15G

echo 0x512 | b2r
1.27K
```

### d2h
#### Type
Python script

#### Usage
```
usage: d2h [-h] [number]

Tiny program to convert a number in decimal to hex.

positional arguments:
  number         decimal number. May be ommitted to read from stdin.

optional arguments:
  -h, --help     Print this message and exit
```

#### Examples
```sh
d2h 42
0x2a

echo 1234 | d2h
0x4d2
```

### h2d
#### Type
symbolic link to d2h

#### Usage
```
usage: h2d [-h] [number]

Tiny program to convert a number in hex to decimal.

positional arguments:
  number         hex number. May be ommitted to read from stdin.

optional arguments:
  -h, --help     Print this message and exit
```

#### Examples
```sh
h2d 42
66

echo 0x1234 | h2d
4660
```

## License
All files are licensed under the MIT license.
