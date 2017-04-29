set -v
echo "world\nits jon" | prepend "hello "

echo "this is\na test" | prepend -f "hello world\n"
