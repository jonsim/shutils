# Table of Contents
 - [shutils](#shutils)
 - [Installation](#installation)
 - [License](#license)
 - [Documentation](#documentation)
  - [b2r](#b2r)
    - [Type](#type)
    - [Usage](#usage)
    - [Examples](#examples)
  - [check-links](#check-links)
    - [Type](#type)
    - [Usage](#usage)
    - [Examples](#examples)
  - [d2h](#d2h)
    - [Type](#type)
    - [Usage](#usage)
    - [Examples](#examples)
  - [h2d](#h2d)
    - [Type](#type)
    - [Usage](#usage)
    - [Examples](#examples)
  - [search](#search)
    - [Type](#type)
    - [Usage](#usage)
    - [Examples](#examples)

# shutils
Collection of my (mostly) sh utils. Where not possible to use sh, bash has been
used instead, but a preference for sh has been made where possible. There are a
few Python files to. All of these have been written with Python 2.7.

&copy; Copyright 2017 Jonathan Simmonds

# Installation
TODO

# License
All files are licensed under the MIT license.

# Documentation
## b2r
#### Type
Python script

#### Usage
```
usage: b2r [-h] [number-of-bytes]

Tiny program to convert a raw number of bytes (either decimal or
prefixed hex) into a human readable form.

positional arguments:
  number-of-bytes    Number of bytes to convert. May be ommitted to
                     read from stdin.

optional arguments:
  -h, --help         Print this message and exit.
```

#### Examples
```sh
b2r 1234567890
1.15G

echo 0x512 | b2r
1.27K
```

## check-links
#### Type
POSIX shell script

#### Usage
```
usage: check-links [-p] [-h] [directory]

Simple application to confirm the validity of symlinks in a directory.

positional arguments:
  directory   Optional directory to search in. If ommitted the current
              working directory is used.

optional arguments:
  -p          Run in script mode, outputing just the name of all
              broken links to stdout. In interactive mode (default)
              output is decorated.
  -h, --help  Print this message and exit.
```

#### Examples
```sh
touch real-file.txt
ln -s real-file.txt real-link.txt
ln -s fake-file.txt fake-link.txt

check-links
WARNING: link './fake-link.txt' is broken.

rm real-file.txt

check-links -p .
./real-link.txt
./fake-link.txt

```

## d2h
#### Type
Python script

#### Usage
```
usage: d2h [-h] [number]

Tiny program to convert a number in decimal to hex.

positional arguments:
  number         decimal number. May be ommitted to read from stdin.

optional arguments:
  -h, --help     Print this message and exit.
```

#### Examples
```sh
d2h 42
0x2a

echo 1234 | d2h
0x4d2
```

## h2d
#### Type
symbolic link to d2h

#### Usage
```
usage: h2d [-h] [number]

Tiny program to convert a number in hex to decimal.

positional arguments:
  number         hex number. May be ommitted to read from stdin.

optional arguments:
  -h, --help     Print this message and exit.
```

#### Examples
```sh
h2d 0x42
66

echo 1234 | h2d
4660
```

## search
#### Type
POSIX shell script

#### Usage
```
usage: search [-i] [-f] [-h] [path] regex

Simple recursive file searcher, wrapping a handful of common find/grep
combos and decorating the output. Ignores .git and .svn directories.

positional arguments:
  path        Optional path to perform the search in. If ommitted the
              current working directory is used.
  regex       Perl-style regular expression to search for. It is
              recommended to pass this in single quotes to prevent
              shell expansion/interpretation of the regex characters.

optional arguments:
  -i          Enable case-insensitive searching.
  -f          Performs the search on the names of files rather than on
              their contents.
  -h, --help  Print this message and exit.
```

#### Examples
```sh
search printers 'def search_result.+:'
printers/decorategrep.py:33  def search_result_from_grep(output):
printers/decoratefind.py:16  def search_results_from_find(output):

search -f -i 'e\.md'
./readme-gen/readme-usage.md
./README.md
```

