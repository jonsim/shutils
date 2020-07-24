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
  - [git-compare-branch](#git-compare-branch)
    - [Type](#type-3)
    - [Usage](#usage-3)
    - [Examples](#examples-3)
  - [h2d](#h2d)
    - [Type](#type-4)
    - [Usage](#usage-4)
    - [Examples](#examples-4)
  - [json-print](#json-print)
    - [Type](#type-5)
    - [Usage](#usage-5)
    - [Examples](#examples-5)
  - [prepend](#prepend)
    - [Type](#type-6)
    - [Usage](#usage-6)
    - [Examples](#examples-6)
  - [tabulate](#tabulate)
    - [Type](#type-7)
    - [Usage](#usage-7)
    - [Examples](#examples-7)
  - [tcgdb](#tcgdb)
    - [Type](#type-8)
    - [Usage](#usage-8)
    - [Examples](#examples-8)
  - [timeit](#timeit)
    - [Type](#type-9)
    - [Usage](#usage-9)
    - [Examples](#examples-9)
  - [wcz](#wcz)
    - [Type](#type-10)
    - [Usage](#usage-10)
    - [Examples](#examples-10)
  - [xwinid](#xwinid)
    - [Type](#type-11)
    - [Usage](#usage-11)
    - [Examples](#examples-11)

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

## git-compare-branch
#### Type
Python script

#### Usage
```
usage: git-compare-branch [-h] [-b] [-n [NUMBER]] [-e] [-m [PATTERN]]
                          [-u [PATTERN]] [--loose-merge-pattern] [-p] [-s]
                          [-S] [-c] [-C] [-f] [-F] [-g] [-G]
                          BRANCH-A BRANCH-B

Finds commits on branch B which are not on branch A. This is able to handle if
B has already been merged down to A. This command runs purely locally and as
such the branches to compare should be checked out and up to date before
running. No state is changed by running this.

positional arguments:
  BRANCH-A              Branch A. This is the branch against which the
                        difference is taken. It must exist locally.
  BRANCH-B              Branch B. This is the branch whose differences are
                        recorded. It must either exist locally or have a
                        corresponding merge commit onto A within the lookback
                        distance. See --merge-pattern and --lookback for
                        details on identifying merge commits and setting the
                        lookback respectively.

optional arguments:
  -h, --help            show this help message and exit
  -b, --both-ways       Print not only the differences from B to A (the
                        default), but also the differences from A to B.
  -n [NUMBER], --lookback [NUMBER]
                        Sets the number of commits to consider in the history.
                        The lookback distance must cover the full lifetime of
                        the branch (i.e. to the fork point). May be set to 0
                        to consider all history (on large repositorys this may
                        take some time). Defaults to 1000.
  -e, --exclude-updates
                        Exclude update commits (merges from A back to B) from
                        all differences. By default all differences are
                        considered.
  -m [PATTERN], --merge-pattern [PATTERN]
                        The stem merge commit pattern to identify the merge
                        commit from B to A. This is only necessary if B does
                        not exist. Defaults to the standard git merge pattern
                        "Merge branch". The merge commit's subject must
                        contain the pattern followed by the merged branch
                        name. It is matched with the following regex:
                        ^PATTERN.*BRANCH_B.*$
  -u [PATTERN], --update-pattern [PATTERN]
                        The stem merge commit pattern to identify any 'update'
                        merge commits from A to B. This is only necessary if
                        using --exclude-updates and if this pattern differs
                        from --merge-pattern. Defaults to the value given in
                        --merge-pattern. All 'update' merge commit subjects
                        must contain the pattern followed by A's name followed
                        by B's name. It is matched with the following regex:
                        ^PATTERN.*BRANCH_A.*$
  --loose-merge-pattern
                        Exclude the branchname from the merge and update
                        patterns (so they match just the pattern given). By
                        default the branchname is included.
  -p, --pretty          Print a short hash and the subject for all commits. By
                        default just the full hash is printed.
  -s, --summary         Print a summary of the status of each branch and their
                        relationship. This is the default.
  -S, --no-summary      Do not print the summary list (see --summary).
  -c, --commits         Print a list of all commits which exist on branch B
                        but not branch A. This is the default.
  -C, --no-commits      Do not print the commit list (see --commits).
  -f, --finger          Print a list of all users who have made commits on
                        branch B.
  -F, --no-finger       Do not print the finger list (see --finger). This is
                        the default.
  -g, --graph           Print a chronological graph of the commits made to
                        branches A and B during their lifetime. This only has
                        an effect if branch B has been merged into branch A,
                        otherwise ignored. Corresponds to the --graph option
                        of git log.
  -G, --no-graph        Do not print the commit graph (see --graph). This is
                        the default.
```

#### Examples
```sh
git branch
* master
  topic2
  topic3


git log --format=oneline --abbrev-commit --date-order
0ff720c Merge branch 'topic3'
1bddb09 N (master)
ff2fa26 Merge branch 'master' into topic3
4517b81 M (topic3)
48adb5a L (master)
14dbda6 K (master)
c3e48a2 I (master)
26a1f0d Merge branch 'topic1'
812f773 H (topic1)
d129d72 Merge branch 'master' into topic1
d1bb781 G (topic1)
f8556f0 E (master)
558f44b F (topic1)
c5aaaa9 D (master)
48b70ff C (master)
7292420 B (master)
d782883 A ()


git-compare-branch master topic3
Summary:
  topic3 still exists
  topic3 forked from master at: 14dbda6586c492639f47c6591b63fbd06e74a363

Commits made on topic3 but not master:
  ff2fa26b1cf17a510b7fc88eb7085b24d53bcf73
  4517b814b7703d7364fd44f736bcb4b5e17be023


git-compare-branch master topic1 --pretty
Summary:
  topic1 no longer exists
  topic1 merged into master at: 26a1f0d8a6c6cddaff2bdd6c7a96430af364cee6
  topic1 forked from master at: c5aaaa948f48d1b8e8e86b850baa1274458da410

Commits made on topic1 but not master:
  812f773 [Fri Jul 24 15:59:55 2020 +0100] H (topic1)
  d129d72 [Fri Jul 24 15:59:55 2020 +0100] Merge branch 'master' into topic1
  d1bb781 [Fri Jul 24 15:59:55 2020 +0100] G (topic1)
  558f44b [Fri Jul 24 15:59:55 2020 +0100] F (topic1)


git-compare-branch master topic1 --both-ways --pretty --summary --commits --finger --graph
Summary:
  topic1 no longer exists
  topic1 merged into master at: 26a1f0d8a6c6cddaff2bdd6c7a96430af364cee6
  topic1 forked from master at: c5aaaa948f48d1b8e8e86b850baa1274458da410

Commits made on topic1 but not master:
  812f773 [Fri Jul 24 15:59:55 2020 +0100] H (topic1)
  d129d72 [Fri Jul 24 15:59:55 2020 +0100] Merge branch 'master' into topic1
  d1bb781 [Fri Jul 24 15:59:55 2020 +0100] G (topic1)
  558f44b [Fri Jul 24 15:59:55 2020 +0100] F (topic1)

Commits made on master but not topic1:
  f8556f0 [Fri Jul 24 15:59:55 2020 +0100] E (master)

Authors of commits on topic1 but not master:
  4 Jonathan Simmonds <jonathansimmonds@gmail.com>

Authors of commits on master but not topic1:
  1 Jonathan Simmonds <jonathansimmonds@gmail.com>

Graph:
  *     26a1f0d [Fri Jul 24 15:59:55 2020 +0100] Merge branch 'topic1'
  |\    
  | *   812f773 [Fri Jul 24 15:59:55 2020 +0100] H (topic1)
  | *   d129d72 [Fri Jul 24 15:59:55 2020 +0100] Merge branch 'master' into topic1
  | |\  
  | |/  
  |/|   
  * |   f8556f0 [Fri Jul 24 15:59:55 2020 +0100] E (master)
  | *   d1bb781 [Fri Jul 24 15:59:55 2020 +0100] G (topic1)
  | *   558f44b [Fri Jul 24 15:59:55 2020 +0100] F (topic1)
  |/    
  *     c5aaaa9 [Fri Jul 24 15:59:55 2020 +0100] D (master)


git-compare-branch master topic1 --both-ways --pretty --summary --commits --finger --graph --exclude-updates
Summary:
  topic1 no longer exists
  topic1 merged into master at: 26a1f0d8a6c6cddaff2bdd6c7a96430af364cee6
  topic1 forked from master at: c5aaaa948f48d1b8e8e86b850baa1274458da410

Commits made on topic1 but not master:
  812f773 [Fri Jul 24 15:59:55 2020 +0100] H (topic1)
  d1bb781 [Fri Jul 24 15:59:55 2020 +0100] G (topic1)
  558f44b [Fri Jul 24 15:59:55 2020 +0100] F (topic1)

Commits made on master but not topic1:
  f8556f0 [Fri Jul 24 15:59:55 2020 +0100] E (master)

Authors of commits on topic1 but not master:
  3 Jonathan Simmonds <jonathansimmonds@gmail.com>

Authors of commits on master but not topic1:
  1 Jonathan Simmonds <jonathansimmonds@gmail.com>

Graph:
  *     26a1f0d [Fri Jul 24 15:59:55 2020 +0100] Merge branch 'topic1'
  |\    
  | *   812f773 [Fri Jul 24 15:59:55 2020 +0100] H (topic1)
  | *   d129d72 [Fri Jul 24 15:59:55 2020 +0100] Merge branch 'master' into topic1
  | |\  
  | |/  
  |/|   
  * |   f8556f0 [Fri Jul 24 15:59:55 2020 +0100] E (master)
  | *   d1bb781 [Fri Jul 24 15:59:55 2020 +0100] G (topic1)
  | *   558f44b [Fri Jul 24 15:59:55 2020 +0100] F (topic1)
  |/    
  *     c5aaaa9 [Fri Jul 24 15:59:55 2020 +0100] D (master)

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

## json-print
#### Type
Python script

#### Usage
```
usage: json-print [-h] [input]

Pretty-prints JSON. Input can either be given as an argument
or via stdin.

optional arguments:
  -h, --help     Print this message and exit.
```

#### Examples
```sh
json-print '{"valuable information":{"answer":42}}'
{
  "valuable information": {
    "answer": 42
  }
}

echo '{"valuable information":{"answer":42}}' | json-print
{
  "valuable information": {
    "answer": 42
  }
}
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

## timeit
#### Type
Python script

#### Usage
```
usage: timeit [-h] [-n NUMBER] [-r REPEAT] [-u {us,ms,s}] [-v] ...

Script to measure the execution time of a command.

positional arguments:
  COMMAND               Command to time.

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        The number of times to execute COMMAND. May be omitted
                        to automatically determine NUMBER.
  -r REPEAT, --repeat REPEAT
                        The number of times to repeat the reading. Defaults to
                        3.
  -u {us,ms,s}, --unit {us,ms,s}
                        The unit of time to output. May be omitted to
                        automatically determine the most appropriate unit.
  -v, --verbose         Verbose output.
```

#### Examples
```sh
timeit find . -name nope
1024 loops, best of 3: 781.236 us per loop

timeit -n 1000 -r 2 "ls > /dev/null"
1000 loops, best of 2: 552.549 us per loop
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
find readme-gen -name '*.txt' -print0 | wcz
1 lines in 1 files

git ls-files -z | wcz -s
2718 lines in 30 files
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
29360129
```

