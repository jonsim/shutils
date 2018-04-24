set -v
find readme-gen -name '*.txt' -print0 | wcz

git ls-files -z | wcz -s
