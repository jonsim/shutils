# (c) Copyright 2017 Jonathan Simmonds
"""Script designed to process grep output (e.g. via a pipe) and prettify it,
organising the result into columns and adding highlighting."""
import sys
import os
import argparse
from ansi_decorate import *

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

class SearchResult(object):
    """Holds the result of a file search and its location.

    Attributes:
        dirname:    string path of directory of match
        basename:   string name of file of match
        lineno:     int 1-indexed line number of match
        result:     string match result
    """
    # The character sequence to place at the truncation point in directory paths
    _DIR_CONT = '...'
    # The character sequence to place at the truncation point in file names
    _FILE_CONT = '...'
    # The character sequence to place at the truncation point in result lines
    _RES_CONT = '...'
    def __init__(self, dirname, basename, lineno, result):
        """Initiailises the SearchResult.

        Args:
            dirname:    string path of directory of match
            basename:   string name of file of match
            lineno:     int 1-indexed line number of match
            result:     string match result
        """
        self.dirname = dirname + os.path.sep
        self.basename = basename
        self.lineno = lineno
        self.result = result.strip()

    def _format_dirname(self, decorate, min_width=None, max_width=None):
        """Internal method to extract and format/truncate/pad the dirname."""
        string = self.dirname
        # If too short, left pad
        if min_width and len(string) < min_width:
            string = ' ' * (min_width - len(string)) + string
        # If too long, truncate from the left
        if max_width and len(string) > max_width:
            string = self._DIR_CONT + string[-(max_width-len(self._DIR_CONT)):]
        # Return, decorating if necessary
        if decorate:
            return ansi_decorate(string, ANSI.FG_YELLOW)
        return string

    def _format_basename(self, decorate, min_width=None, max_width=None):
        """Internal method to extract and format/truncate/pad the basename."""
        string = self.basename
        # If too short, right pad
        if min_width and len(string) < min_width:
            string = string + ' ' * (min_width - len(string))
        # If too long, truncate from the right
        if max_width and len(string) > max_width:
            string = string[:-(max_width-len(self._FILE_CONT))] + self._FILE_CONT
        # Return, decorating if necessary
        if decorate:
            return ansi_decorate(string, ANSI.BOLD, ANSI.FG_YELLOW)
        return string

    def _format_lineno(self, decorate, min_width=None):
        """Internal method to extract and format/truncate/pad the lineno."""
        string = ':' + str(self.lineno)
        # If too short, right pad
        if min_width and len(string) < min_width:
            string = string + ' ' * (min_width - len(string))
        # Return, decorating if necessary
        if decorate:
            return ansi_decorate(string, ANSI.FG_YELLOW)
        return string

    def format_fileinfo(self, decorate, min_width=None, max_width=None, min_lineno_width=None):
        """Formats the fileinfo column, decorating, truncating and padding it.

        Args:
            decorate:           bool whether or not to decorate the string with
                ANSI escape codes (e.g. for terminal display).
            min_width:          int minimum character width to draw the column
                to. Additional width will be made up by padding.
            max_width:          int maximum character width to draw the column
                to. Additional width will be removed by truncating.
            min_lineno_width:   int minimum width to draw the line number field
                to. Additional width will be made up by padding.

        Returns:
            The formatted string.
        """
        if not max_width:
            string = self._format_dirname(decorate) + \
                     self._format_basename(decorate) + \
                     self._format_lineno(decorate, min_width=min_lineno_width)
        else:
            string = self._format_lineno(decorate, min_width=min_lineno_width)
            # While we can afford to add more to the string, keep adding
            curlen = len(ansi_undecorate(string))
            if curlen < max_width:
                string = self._format_basename(decorate, max_width=max_width-curlen) + string
            curlen = len(ansi_undecorate(string))
            if curlen < max_width:
                string = self._format_dirname(decorate, max_width=max_width-curlen) + string
        # If too short, right pad
        curlen = len(ansi_undecorate(string))
        if min_width and curlen < min_width:
            string = string + ' ' * (min_width - curlen)
        return string

    def format_result(self, decorate, term, min_width=None, max_width=None):
        """Formats the result column, decorating, truncating and padding it.

        Args:
            decorate:           bool whether or not to decorate the string with
                ANSI escape codes (e.g. for terminal display).
            min_width:          int minimum character width to draw the column
                to. Additional width will be made up by padding.
            max_width:          int maximum character width to draw the column
                to. Additional width will be removed by truncating.

        Returns:
            The formatted string.
        """
        import re
        string = self.result
        # If too short, right pad
        if min_width and len(string) < min_width:
            string = string + ' ' * (min_width - len(string))
        # If too long, truncate
        if max_width and len(string) > max_width:
            # If we've been given the search truncate intelligently, trying to
            # retain at least one match. Otherwise just truncate from the right
            match = re.search(term, string) if term else None
            start_pos = match.start(0) - 10 if match and match.start(0) > 10 else 0
            end_pos = start_pos + max_width
            if end_pos > len(string):
                start_pos -= end_pos - len(string)
                end_pos = len(string)
            start_trunc = start_pos > 0
            end_trunc = end_pos < len(string)
            if start_trunc:
                start_pos += len(self._RES_CONT)
            if end_trunc:
                end_pos -= len(self._RES_CONT)
            string = string[start_pos:end_pos]
            if start_trunc:
                string = self._RES_CONT + string
            if end_trunc:
                string = string + self._RES_CONT
        # Return, decorating if necessary
        if decorate and term:
            # Highlight search term
            matches = re.split('(' + term + ')', string)
            for i in range(1, len(matches), 2):
                matches[i] = ansi_decorate(matches[i], ANSI.BOLD, ANSI.FG_RED)
            return ''.join(matches)
        return string


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

def print_result(result, term, decorate, console_width, results_max):
    """Prints the SearchResult to stdout.

    Args:
        result:         SearchResult object to print.
        term:           string search term used to produce this result. May be
            None if unknown.
        decorate:       bool whether or not to decorate the string with ANSI
            escape codes (e.g. for terminal display).
        console_width:  int max character width the current console is able to
            display for output. Attempts will be made to truncate or fit to this
            if possible (based on 'minimisation' global constants).
        results_max:    SearchResultsMax object containing the maxima
            information from all processed SearchResults.

    Returns:
        None
    """
    fileinfo = None
    fresult = None
    # If the longest line can fit on the screen, print normally
    if results_max.total_len <= console_width:
        fileinfo = result.format_fileinfo(decorate, \
                        min_width=results_max.fileinfo_len + MIN_COL_SPACING, \
                        min_lineno_width=results_max.lineno_len)
        fresult = result.format_result(decorate, term)
    min_fileinfo_width = min(MAX_MINIMISATION, results_max.fileinfo_len)
    min_fresult_width = min(MAX_MINIMISATION, results_max.fresult_len)
    # If we still haven't got a result but can minimise fileinfo, try to print
    if not (fileinfo and result) and MINIMISE_FILEINFO and not MINIMISE_RESULT:
        # Does being allowed to minimise the fileinfo even help?
        if results_max.fresult_len <= console_width - min_fileinfo_width - MIN_COL_SPACING:
            fileinfo = result.format_fileinfo(decorate, \
                            min_width=console_width - results_max.fresult_len, \
                            max_width=console_width - results_max.fresult_len - MIN_COL_SPACING, \
                            min_lineno_width=results_max.lineno_len)
            fresult = result.format_result(decorate, term)
    # If we still haven't got a result but can minimise result, try to print
    if not (fileinfo and result) and MINIMISE_RESULT and not MINIMISE_FILEINFO:
        # Does being allowed to minimise the result even help?
        if results_max.fileinfo_len <= console_width - min_fresult_width - MIN_COL_SPACING:
            fileinfo = result.format_fileinfo(decorate, \
                            min_width=results_max.fileinfo_len + MIN_COL_SPACING, \
                            min_lineno_width=results_max.lineno_len)
            fresult = result.format_result(decorate, term, \
                            max_width=console_width - results_max.fileinfo_len - MIN_COL_SPACING)
    # If we still haven't got a result but can minimise both sides, try to print
    if not (fileinfo and result) and MINIMISE_FILEINFO and MINIMISE_RESULT:
        # Does being allowed to minimise both sides even help?
        if console_width >= min_fileinfo_width + MIN_COL_SPACING + min_fresult_width:
            flx_fileinfo_width = min(term / 3, results_max.fileinfo_len)
            flx_fresult_width = console_width - flx_fileinfo_width - MIN_COL_SPACING
            fileinfo = result.format_fileinfo(decorate, \
                            min_width=flx_fileinfo_width + MIN_COL_SPACING, \
                            max_width=flx_fileinfo_width, \
                            min_lineno_width=results_max.lineno_len)
            fresult = result.format_result(decorate, term, \
                            max_width=flx_fresult_width)
    # If all else fails, just print the results on separate lines
    if not (fileinfo and result):
        fileinfo = result.format_fileinfo(decorate, \
                        max_width=console_width if FIT_TO_CONSOLE else None) + '\n'
        fresult = result.format_result(decorate, term, \
                        max_width=console_width if FIT_TO_CONSOLE else None) + '\n'
    print fileinfo + fresult

def console_size():
    """Derives the current console's size.

    NB: Taken from http://stackoverflow.com/a/3010495

    Returns:
        (width, height) of the current console.
    """
    import fcntl, termios, struct
    try:
        h, w, hp, wp = struct.unpack('HHHH',
                                     fcntl.ioctl(1, termios.TIOCGWINSZ,
                                                 struct.pack('HHHH', 0, 0, 0, 0)))
    except IOError:
        w, h = (80, 40)
    return w, h

def print_results(results, term, decorate):
    """Prints all the SearchResults to stdout.

    Args:
        results: list of SearchResult objects to print.
        term:           string search term used to produce this result. May be
            None if unknown.
        decorate:       bool whether or not to decorate the string with ANSI
            escape codes (e.g. for terminal display).

    Returns:
        None
    """
    class SearchResultsMax(object):
        """Holds the maxima information of a number of SearchResult objects.

        Attributes:
            lineno_len:     The longest line number field length.
            fileinfo_len:   The longest file-info column length.
            fresult:        The longest formatted result column length.
        """
        def __init__(self, search_results):
            lineno = max([r.lineno for r in search_results])
            self.lineno_len = len(str(lineno)) + 1
            self.fileinfo_len = max([len(r.format_fileinfo(False, \
                    min_lineno_width=self.lineno_len)) for r in search_results])
            self.fresult_len = max([len(r.format_result(False, None)) for r in search_results])
            self.total_len = self.fileinfo_len + self.fresult_len

    console_width, console_height = console_size()
    max_results = SearchResultsMax(results)
    for result in results:
        print_result(result, term, decorate, console_width, max_results)

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
        print_results(results, args.term, not args.script_mode)


# Entry point.
if __name__ == "__main__":
    main()
