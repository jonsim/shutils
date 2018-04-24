set -v
timeit find . -name nope

timeit -n 1000 -r 2 "ls > /dev/null"
