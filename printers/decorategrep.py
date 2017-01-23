# (c) Copyright 2017 Jonathan Simmonds
"""Script designed to process grep output (e.g. via a pipe) and prettify it,
organising the result into columns and adding highlighting."""
import sys
import os
import argparse
from console import console_size
from search_result import SearchResult
from search_result import SearchResultsMax

# Whether to allow 'minimising' the file-info (file path and line number) column
# if the file-info and result columns cannot otherwise be printed on a single
# line. The column is minimised by truncating with SearchResult._DIR_CONT and
# SearchResult._FILE_CONT
# If this is false or truncation would otherwise reduce the column below
# MAX_MINIMISATION, the file-info/result columns are printed in separate lines.
MINIMISE_FILEINFO = False
# Whether to allow 'minimising' the result column if the file-info and result
# columns cannot otherwise be printed on a single line. The column is minimised
# by truncating with SearchResult._RES_CONT
# If this is false or truncation would otherwise reduce the column below
# MAX_MINIMISATION, the file-info/result columns are printed in separate lines.
MINIMISE_RESULT = True
# If the file-info/result columns are printed on separate lines, whether to
# limite these to the width of the terminal.
FIT_TO_CONSOLE = True
# The minimum number of characters a minimisation may reduce a string to.
MAX_MINIMISATION = 16
# The minimum number of spacing between file-info and result columns.
MIN_COL_SPACING = 2


def search_result_from_grep(output):
    """Creates a SearchResult object from the output from a grep command.

    NB: This relies on grep being called with at least args 'HIZns'

    Args:
        output: The grep output string to process.

    Returns:
        The initialised SearchResult.
    """
    out_split = output.split('\0', 1)
    if len(out_split) != 2:
        raise Exception('Line does not look like grep -HIZns output: ' + output)
    line_split = out_split[1].split(':', 1)
    if len(out_split) != 2:
        raise Exception('Line does not look like grep -HIZns output: ' + output)
    basename = os.path.basename(out_split[0])
    dirname = os.path.dirname(out_split[0])
    lineno = int(line_split[0])
    result = line_split[1]
    return SearchResult(dirname, basename, lineno, result)

def print_result(result, term, ignore_case, decorate, console_width, results_max, condense_result=MINIMISE_RESULT):
    """Prints the SearchResult to stdout.

    Args:
        result:             SearchResult object to print.
        term:               string search term used to produce this result. May
            be None if unknown.
        ignore_case:        bool whether or not to ignore the case when
            highlighting the match. Only meaningful if term is not None.
        decorate:           bool whether or not to decorate the string with ANSI
            escape codes (e.g. for terminal display).
        console_width:      int max character width the current console is able
            to display for output. Attempts will be made to truncate or fit to
            this if possible (based on 'minimisation' global constants).
        results_max:        SearchResultsMax object containing the maxima
            information from all processed SearchResults.
        condense_result:    Whether to allow 'minimising' the result column if
            the file-info and result columns cannot otherwise be printed on a
            single line.

    Returns:
        None
    """
    fileinfo = None
    fresult = None
    # If the longest line can fit on the screen, print normally
    if results_max.fileinfo_len + MIN_COL_SPACING + results_max.fresult_len <= console_width:
        fileinfo = result.format_fileinfo(decorate, \
                        min_width=results_max.fileinfo_len + MIN_COL_SPACING, \
                        min_lineno_width=results_max.lineno_len)
        fresult = result.format_result(term, ignore_case, decorate)
    min_fileinfo_width = min(MAX_MINIMISATION, results_max.fileinfo_len)
    min_fresult_width = min(MAX_MINIMISATION, results_max.fresult_len)
    # If we still haven't got a result but can minimise fileinfo, try to print
    if not (fileinfo and result) and MINIMISE_FILEINFO and not condense_result:
        # Does being allowed to minimise the fileinfo even help?
        if results_max.fresult_len <= console_width - min_fileinfo_width - MIN_COL_SPACING:
            fileinfo = result.format_fileinfo(decorate, \
                            min_width=console_width - results_max.fresult_len, \
                            max_width=console_width - results_max.fresult_len - MIN_COL_SPACING, \
                            min_lineno_width=results_max.lineno_len)
            fresult = result.format_result(term, ignore_case, decorate)
    # If we still haven't got a result but can minimise result, try to print
    if not (fileinfo and result) and condense_result and not MINIMISE_FILEINFO:
        # Does being allowed to minimise the result even help?
        if results_max.fileinfo_len <= console_width - min_fresult_width - MIN_COL_SPACING:
            fileinfo = result.format_fileinfo(decorate, \
                            min_width=results_max.fileinfo_len + MIN_COL_SPACING, \
                            min_lineno_width=results_max.lineno_len)
            fresult = result.format_result(term, ignore_case, decorate, \
                            max_width=console_width - results_max.fileinfo_len - MIN_COL_SPACING)
    # If we still haven't got a result but can minimise both sides, try to print
    if not (fileinfo and result) and MINIMISE_FILEINFO and condense_result:
        # Does being allowed to minimise both sides even help?
        if console_width >= min_fileinfo_width + MIN_COL_SPACING + min_fresult_width:
            flx_fileinfo_width = min(term / 3, results_max.fileinfo_len)
            flx_fresult_width = console_width - flx_fileinfo_width - MIN_COL_SPACING
            fileinfo = result.format_fileinfo(decorate, \
                            min_width=flx_fileinfo_width + MIN_COL_SPACING, \
                            max_width=flx_fileinfo_width, \
                            min_lineno_width=results_max.lineno_len)
            fresult = result.format_result(term, ignore_case, decorate, \
                            max_width=flx_fresult_width)
    # If all else fails, just print the results on separate lines
    if not (fileinfo and result):
        fileinfo = result.format_fileinfo(decorate, \
                        max_width=console_width if FIT_TO_CONSOLE else None) + '\n'
        fresult = result.format_result(term, ignore_case, decorate, \
                        max_width=console_width if FIT_TO_CONSOLE else None) + '\n'
    print fileinfo + fresult

def print_results(results, term, ignore_case, decorate, condense_result=MINIMISE_RESULT):
    """Prints all the SearchResults to stdout.

    Args:
        results:            list of SearchResult objects to print.
        term:               string search term used to produce this result. May
            be None if unknown.
        ignore_case:        bool whether or not to ignore the case when
            highlighting the match. Only meaningful if term is not None.
        decorate:       bool whether or not to decorate the string with ANSI
            escape codes (e.g. for terminal display).
        condense_result:    Whether to allow 'minimising' the result column if
            the file-info and result columns cannot otherwise be printed on a
            single line.

    Returns:
        None
    """
    console_width, console_height = console_size()
    max_results = SearchResultsMax(results)
    for result in results:
        print_result(result, term, ignore_case, decorate, console_width, max_results,
                     condense_result=condense_result)

def main():
    """Main method."""
    # Handle command line
    parser = argparse.ArgumentParser(description='Takes the output of a grep call ' \
                                    'which uses at least the -HIZns flags and prints '
                                    'it into a prettier format.')
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
                        'the search term (-t) is provided.')
    parser.add_argument('-v', dest='full_result', action='store_const', const=True,
                        default=False,
                        help='Enable verbose, full replication of the result column, '
                        'even if it means taking multiple lines per match (by '
                        'default the result will be condensed to keep one line per '
                        'match if possible).')
    args = parser.parse_args()

    results = []
    if args.file:
        with open(args.file, 'r') as f:
            for line in f:
                results.append(search_result_from_grep(line))
    else:
        for line in sys.stdin:
            results.append(search_result_from_grep(line))
    if results:
        print_results(results, args.term, args.ignore_case, not args.script_mode,
                      not args.full_result)


# Entry point.
if __name__ == "__main__":
    main()
