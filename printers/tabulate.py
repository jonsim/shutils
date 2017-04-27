# (c) Copyright 2017 Jonathan Simmonds
"""Script designed to split and tabulate streamed input."""
import argparse     # ArgumentParser
import sys          # stdin

def tabulate(rows, first_row_are_headers):
    # Count the maximum number of columns.
    max_cols = max([len(r) for r in rows])
    # Count the maximum width of each cell.
    max_cells = [max([len(r[i]) if i < len(r) else 0 for r in rows]) for i in range(0, max_cols)]
    # Print.
    output = []
    first_row = True
    for row in rows:
        output.append(" | ".join([row[i].rjust(max_cells[i]) if i < len(row) else " " * max_cells[i] for i in range(0, max_cols)]))
        if first_row_are_headers and first_row:
            output.append("-|-".join(["-" * l for l in max_cells]))
            first_row = False
    return '\n'.join(output)

def main():
    """Main method."""
    # Handle command line
    parser = argparse.ArgumentParser(description='Takes input on stdin, splits it on ' \
                                    'a delimiter and tabulates it into rows and ' \
                                    'columns.')
    parser.add_argument('file', type=str, default=None, nargs='?',
                        help='The file to read. May be ommitted to read from stdin.')
    parser.add_argument('-r', dest='row_delim', type=str, nargs='?', const='\n', default='\n',
                        help='Delimiter to split rows on. Defaults to \'\\n\'.')
    parser.add_argument('-c', dest='col_delim', type=str, nargs='?', const=' ', default=' ',
                        help='Delimiter to split columns on. Defaults to \' \'.')
    parser.add_argument('-H', dest='row1_headers', action='store_const', const=True,
                        default=False,
                        help='Use the first row as headers. By default no headers ' \
                        'are drawn.')
    args = parser.parse_args()

    # Read input.
    lines = []
    if args.file:
        with open(args.file, 'r') as f:
            lines = f.read()
    else:
        lines = sys.stdin.read()

    # Process input.
    rows = lines.split(args.row_delim)
    for i in range(0, len(rows)):
        rows[i] = rows[i].split(args.col_delim)

    # Tabulate.
    print tabulate(rows, args.row1_headers)

# Entry point.
if __name__ == "__main__":
    main()
