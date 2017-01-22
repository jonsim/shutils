# Table of Contents
 - [shutils](#shutils)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [License](#license)
 - [Documentation](#documentation)
  - [b2r](#b2r)
    - [Type](#type)
    - [Usage](#usage)
    - [Examples](#examples)
  - [check-links](#check-links)
    - [Type](#type-1)
    - [Usage](#usage-1)
    - [Examples](#examples-1)
  - [d2h](#d2h)
    - [Type](#type-2)
    - [Usage](#usage-2)
    - [Examples](#examples-2)
  - [h2d](#h2d)
    - [Type](#type-3)
    - [Usage](#usage-3)
    - [Examples](#examples-3)
  - [search](#search)
    - [Type](#type-4)
    - [Usage](#usage-4)
    - [Examples](#examples-4)
  - [tcgdb](#tcgdb)
    - [Type](#type-5)
    - [Usage](#usage-5)
    - [Examples](#examples-5)
  - [xwinid](#xwinid)
    - [Type](#type-6)
    - [Usage](#usage-6)
    - [Examples](#examples-6)

# shutils
Collection of my sh utils, for use in all POSIX compliant shells. All
applications have been implemented either as a POSIX compliant sh script, or as
a Python script.

&copy; Copyright 2017 Jonathan Simmonds

## Dependencies
* Python 2.7+

## Installation
TODO

## License
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

## tcgdb
#### Type
POSIX shell script

#### Usage
```
usage: tcgdb [-h] program [gdb-arg [gdb-arg [...]]]

Basic wrapper on top of cgdb to separate program output into a tmux
panel. The Rolls Royce of terminal debuggers.

positional arguments:
  program     Path to the application to debug.
  gdb-args    All additional arguments will be passed as gdb options to
              cgdb (which will pass them straight through to gdb). If
              tcgdb immediately exits these commands are likely invalid.

optional arguments:
  -h, --help  Print this message and exit.
```

#### Examples
```sh
tcgdb someapp.out
```

## xwinid
#### Type
POSIX shell script

#### Usage
```
usage: xwinid [window-name]

Tiny wrapper on top of xwininfo to grab just the Window ID in decimal.

positional arguments:
  window-name     Optional name of the window to query. If ommitted the
                  cursor will be used to select the window to query.

optional arguments:
  -h, --help  Print this message and exit.
```

#### Examples
```sh
xwinid compiz
29360135
```

