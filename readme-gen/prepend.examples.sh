set -v
echo "world\nit's jon" | prepend "hello "

echo "this is\na test" | prepend -f "hello world\n"
