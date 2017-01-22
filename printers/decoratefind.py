# (c) Copyright 2017 Jonathan Simmonds
"""Script designed to process find output (e.g. via a pipe) and prettify it,
organising the result into columns and adding highlighting."""
import sys
import argparse
from console import console_size
from search_result import SearchResult

# Whether to allow 'minimising' the result column if it cannot otherwise be
# printed on a single line. The column is minimised by truncating with
# SearchResult._RES_CONT
# If this is false the result column will wrap multiple lines.
MINIMISE_RESULT = False


def search_results_from_find(output):
    """Creates a list of SearchResults from the output from a find command.

    NB: This relies on find being called with -print0

    Args:
        output: The find output string to process.

    Returns:
        A list of initialised SearchResult objects.
    """
    out_split = output.split('\0')
    results = []
    for split in out_split:
        if split:
            results.append(SearchResult(None, None, None, split))
    return results

def print_result(result, term, ignore_case, decorate, console_width):
    """Prints the SearchResult to stdout.

    Args:
        result:         SearchResult object to print.
        term:           string search term used to produce this result. May be
            None if unknown.
        ignore_case:    bool whether or not to ignore the case when highlighting
            the match. Only meaningful if term is not None.
        decorate:       bool whether or not to decorate the string with ANSI
            escape codes (e.g. for terminal display).
        console_width:  int max character width the current console is able to
            display for output. Attempts will be made to truncate or fit to this
            if possible (based on 'minimisation' global constants).

    Returns:
        None
    """
    max_width = console_width if MINIMISE_RESULT else None
    print result.format_result(term, ignore_case, decorate, max_width=max_width)

def print_results(results, term, ignore_case, decorate):
    """Prints all the SearchResults to stdout.

    Args:
        results: list of SearchResult objects to print.
        term:           string search term used to produce this result. May be
            None if unknown.
        ignore_case:    bool whether or not to ignore the case when highlighting
            the match. Only meaningful if term is not None.
        decorate:       bool whether or not to decorate the string with ANSI
            escape codes (e.g. for terminal display).

    Returns:
        None
    """
    console_width, console_height = console_size()
    for result in results:
        print_result(result, term, ignore_case, decorate, console_width)

def main():
    """Main method."""
    # Handle command line
    parser = argparse.ArgumentParser(description='Takes the output of a find call ' \
                                    'which uses -print0 prints it into a prettier '
                                    'format.')
    parser.add_argument('file', type=str, default=None, nargs='?',
                        help='The file to read. May be ommitted to read from stdin.')
    parser.add_argument('-p', dest='script_mode', action='store_const', const=True,
                        default=False,
                        help='Run in script mode, outputting the results without ANSI '
                        'escape code decoration. In iteractive mode (default) output '
                        'is decorated.')
    parser.add_argument('-t', dest='term', default=None,
                        help='The search term used in generating the output. This is '
                        'optional, it is only used for highlighting the matches in '
                        'the results.')
    parser.add_argument('-i', dest='ignore_case', action='store_const', const=True,
                        default=False,
                        help='Enable case-insensitive searching. Only meaningful if '
                        'the search term is provided (-t).')
    args = parser.parse_args()

    results = []
    if args.file:
        with open(args.file, 'r') as f:
            for line in f:
                results += search_results_from_find(line)
    else:
        results = search_results_from_find(sys.stdin.read())
    if results:
        print_results(results, args.term, args.ignore_case, not args.script_mode)


# Entry point.
if __name__ == "__main__":
    main()
