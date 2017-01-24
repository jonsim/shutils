set -v
find printers -name '*.py' -print0 | wcz

git ls-files -z | wcz -s
