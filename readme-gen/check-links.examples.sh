touch real-file.txt
ln -s real-file.txt real-link.txt
ln -s fake-file.txt fake-link.txt

check-links

rm real-file.txt

check-links -p .
set +v
rm -f real-file.txt real-link.txt fake-link.txt
