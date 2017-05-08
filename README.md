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
  - [prepend](#prepend)
    - [Type](#type-4)
    - [Usage](#usage-4)
    - [Examples](#examples-4)
  - [search](#search)
    - [Type](#type-5)
    - [Usage](#usage-5)
    - [Examples](#examples-5)
  - [tabulate](#tabulate)
    - [Type](#type-6)
    - [Usage](#usage-6)
    - [Examples](#examples-6)
  - [tcgdb](#tcgdb)
    - [Type](#type-7)
    - [Usage](#usage-7)
    - [Examples](#examples-7)
  - [wcz](#wcz)
    - [Type](#type-8)
    - [Usage](#usage-8)
    - [Examples](#examples-8)
  - [xwinid](#xwinid)
    - [Type](#type-9)
    - [Usage](#usage-9)
    - [Examples](#examples-9)

# shutils
Collection of my sh utils, for use in all POSIX compliant shells. All
applications have been implemented either as a POSIX compliant sh script, or as
a Python script requiring at most Python 2.7.

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

## prepend
#### Type
Python script

#### Usage
```
usage: prepend [-h] [-f] [string]

Takes input on stdin and prepends a string to either each line or just the
initial line.

positional arguments:
  string      The string to prepend.

optional arguments:
  -h, --help  show this help message and exit
  -f          Prepend the string to just the first line of input. By default
              the string is prepended to each line.
```

#### Examples
```sh
echo "world\nits jon" | prepend "hello "
hello world
hello its jon

echo "this is\na test" | prepend -f "hello world\n"
hello world
this is
a test
```

## search
#### Type
POSIX shell script

#### Usage
```
usage: search [-i] [-f] [-v] [-h] [path] regex

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
  -v          Enable verbose, full replication of the result column,
              even if it means taking multiple lines per match (by
              default the result will be condensed to keep one line per
              match if possible).
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

## tabulate
#### Type
Python script

#### Usage
```
usage: tabulate [-h] [-r [ROW_DELIM]] [-c [COL_DELIM]] [-H] [-b] [-f [FORMAT]]
                [-s [{minimal,basic,basic-grid,fancy,fancy-grid,html,html-full}]]
                [file]

Takes input from a file or stdin, splits it into rows and columns on
respective delimiters and prints the result in a table in a number of formats
and styles.

positional arguments:
  file                  The file to read. May be ommitted to read from stdin.

optional arguments:
  -h, --help            show this help message and exit
  -r [ROW_DELIM]        Delimiter to split rows on. Defaults to '\n'.
  -c [COL_DELIM]        Delimiter to split columns on. Defaults to ' '.
  -H                    Use the first row as headers. By default no headers
                        are drawn.
  -b                    Surround the table with a border (providing the style
                        supports it). "minimal" and "html" styles do not
                        support this. By default no border is drawn.
  -f [FORMAT]           Formatting to apply to the columns. This should be a
                        comma-separated list of format strings for each column
                        (any columns not covered will be removed). Format
                        strings may contain a number (representing the maximum
                        column width) and/or a character (representing the
                        column alignment, 'c' for centered, 'l' for left, 'r'
                        for right). E.g. "10r,15,c". By default all columns
                        are unlimited width, left aligned.
  -s [{minimal,basic,basic-grid,fancy,fancy-grid,html,html-full}]
                        Style of table to draw. Defaults to "basic". "minimal"
                        uses purely spaces to align the elements with an
                        underline for headers. "basic" separates columns with
                        a vertical bar and the header with an underline.
                        "basic-grid" separates columns with a vertical bar and
                        all rows with a horizontal bar, using a heavier bar
                        for headers. "fancy" is similar to basic but using
                        non-ASCII characters for the decorations. "fancy-grid"
                        is similar to basic-grid but using non-ASCII
                        characters for the decoration. "html" produces a HTML
                        table element. "html-full" produces a standalone HTML
                        page with the table on it.
```

#### Examples
```sh
echo "basic tabulate test\nto show\nthe  functionality" | tabulate
basic | tabulate | test         
to    | show     |              
the   |          | functionality

echo "basic tabulate test\nto show\nthe  functionality" | tabulate -H
basic | tabulate | test         
------+----------+--------------
to    | show     |              
the   |          | functionality

tabulate -s basic-grid -H -b -f ',16c,r' -c '\t' tabulate-test.txt
+=========+==================+=====================================+
| Header1 |     Header2      |                                     |
+=========+==================+=====================================+
| hello   |      world       |                             foo bar |
+---------+------------------+-------------------------------------+
|         | this is a longer | meanwhile this line is unrestricted |
|         | and more varied  |                                     |
|         | line limited to  |                                     |
|         |  16 characters   |                                     |
+---------+------------------+-------------------------------------+
| is      |        a         |                                test |
+---------+------------------+-------------------------------------+
| of      |     tabulate     |                                     |
+---------+------------------+-------------------------------------+
| very    |      tricky      |                                     |
+---------+------------------+-------------------------------------+

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

## wcz
#### Type
POSIX shell script

#### Usage
```
usage: wcz [-s] [-h]

Basic wrapper on top of wc which reads NUL-terminated filenames from
stdin until EOF when it prints a line- (using wc) and file-count.

optional arguments:
  -s          Print only the final summary line, not the full line-count.
  -h, --help  Print this message and exit.
```

#### Examples
```sh
find printers -name '*.py' -print0 | wcz
  195 printers/decorategrep.py
   21 printers/console.py
  181 printers/search_result.py
  110 printers/decoratefind.py
   74 printers/ansi_decorate.py
581 lines in 5 files

git ls-files -z | wcz -s
2099 lines in 31 files
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

