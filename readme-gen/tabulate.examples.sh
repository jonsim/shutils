set +v
echo "Header1\tHeader2" > tabulate-test.txt
echo "hello\tworld\tfoo bar" >> tabulate-test.txt
echo "\tthis is a longer and more varied line limited to 16 characters\tmeanwhile this line is unrestricted" >> tabulate-test.txt
echo "is\ta\ttest" >> tabulate-test.txt
echo "of\ttabulate" >> tabulate-test.txt
echo "very\ttricky" >> tabulate-test.txt
set -v
echo "basic tabulate test\nto show\nthe  functionality" | tabulate

echo "basic tabulate test\nto show\nthe  functionality" | tabulate -H

tabulate -s basic-grid -H -b -f ',16c,r' -c '\t' tabulate-test.txt
set +v
rm -f tabulate-test.txt
