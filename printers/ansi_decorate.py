# (c) Copyright 2017 Jonathan Simmonds

def enum(**enums):
    """Very basic enum constructor.

    Args:
        enums:  list of mappings of enum names to values.

    Returns:
        Basic enum representation.
    """
    return type('Enum', (), enums)

ANSI = enum(
    RESET =       0, # Resets text
    BOLD =        1, # Bold / increased intensity
    ITALIC =      3, # Italic text (not widely supported)
    UNDERLINE =   4, # Single underline
    BLINK =       5, # Blinks text
    FG_BLACK =   30, # Foreground text black
    FG_RED =     31, # Foreground text red
    FG_GREEN =   32, # Foreground text green
    FG_YELLOW =  33, # Foreground text yellow
    FG_BLUE =    34, # Foreground text blue
    FG_MAGENTA = 35, # Foreground text magenta
    FG_CYAN =    36, # Foreground text cyan
    FG_WHITE =   37, # Foreground text white
    BG_BLACK =   40, # Background highlight black
    BG_RED =     41, # Background highlight red
    BG_GREEN =   42, # Background highlight green
    BG_YELLOW =  43, # Background highlight yellow
    BG_BLUE =    44, # Background highlight blue
    BG_MAGENTA = 45, # Background highlight magenta
    BG_CYAN =    46, # Background highlight cyan
    BG_WHITE =   47, # Background highlight white
    )

def ansi_decorate(string, *formats):
    """Decorates a string using ANSI escape codes given some format enums.

    Calling len(s) on a string which has been decorated in this manner will not
    return the printed width. Call len(ansi_undecorate(s)) to achieve this.

    Args:
        string:     string to decorate.
        formats:    any number of format enums to apply to the string.

    Returns:
        Decorated representation of string.
    """
    # If no formats have been given, do nothing
    if len(formats) == 0:
        return string
    # Otherwise construct the start code
    start = "\033["
    for fmt in formats:
        start += str(fmt) + ';'
    # Remove final ';', append an 'm'
    start = start[:-1] + 'm'
    # Hard coded reset code to finish
    end = "\033[0m"
    return start + string + end

def ansi_undecorate(string):
    """Removes all ANSI escape codes from a given string.

    Args:
        string: string to 'undecorate'.

    Returns:
        Undecorated, plain string.
    """
    import re
    return re.sub(r'\033\[[^m]+m', '', string)
