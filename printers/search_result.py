# (c) Copyright 2017 Jonathan Simmonds
"""Module providing classes for holding file search results and decorating them."""
import os
from ansi_decorate import *

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
        self.dirname = dirname + os.path.sep if dirname else None
        self.basename = basename
        self.lineno = lineno
        self.result = result.strip() if result else None

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
        if not (self.basename and self.dirname):
            return ''
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
        if not self.result:
            return ''
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
            string = ''.join(matches)
        return string


class SearchResultsMax(object):
    """Holds the maxima information of a number of SearchResult objects.

    Attributes:
        lineno_len:     The longest line number field length.
        fileinfo_len:   The longest file-info column length.
        fresult_len:    The longest formatted result column length.
    """
    def __init__(self, search_results):
        lineno = max([r.lineno for r in search_results])
        self.lineno_len = len(str(lineno)) + 1 if lineno else None
        self.fileinfo_len = max([len(r.format_fileinfo(False, \
                min_lineno_width=self.lineno_len)) for r in search_results])
        self.fresult_len = max([len(r.format_result(False, None)) for r in search_results])
