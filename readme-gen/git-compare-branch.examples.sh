# (c) Copyright 2017 Jonathan Simmonds
set +v

#
# First setup the test repo.
#

write_file()
{
    # $1 filename; $2 content
    [ -d $(dirname "$1") ] || mkdir -p $(dirname "$1")
    echo "$2" > "$1"
}

write_and_commit()
{
    # $1 filename; $2 content
    # Form message and increment counter
    BRANCH_NAME=$(git branch | grep '* ' | cut -d ' ' -f 2)
    COMMIT_CHAR=$(python -c "print chr(64 + $COMMIT_NUMBER)")
    COMMIT_MSG="$COMMIT_CHAR ($BRANCH_NAME)"
    COMMIT_NUMBER=$(expr $COMMIT_NUMBER + 1)
    # Write file, add and commit
    write_file "$1" "$2"
    git add "$1" > /dev/null
    git commit -m "$COMMIT_MSG" > /dev/null
}

merge_branch()
{
    # $1 branch
    git merge --no-edit --commit --no-ff $1 > /dev/null
}

COMMIT_NUMBER=1
REPONAME="test-repo"

rm -fr "$REPONAME"
mkdir -p "$REPONAME"
cd "$REPONAME"
git init > /dev/null

# First commit
write_and_commit root_file.txt "root"

# Make subdirs
write_and_commit subdir1/file1.txt "hello world"
write_and_commit subdir1/file2.txt "this is a test"
write_and_commit subdir2/file1.txt "another file"

# Branch
git branch topic1

# Add some more commits on master
write_and_commit subdir1/file1.txt "hello world\nagain"

# Add some more commits on topic1
git checkout topic1 > /dev/null 2>&1
write_and_commit subdir1/file2.txt "this is an easy test"
write_and_commit subdir2/file1.txt "another file\nwith content"

# Merge changes from master up to topic1
merge_branch master

# Do another commit on topic1
write_and_commit subdir1/file2.txt "quick fix"

# Merge changes from master up to topic1 again
merge_branch master

# Merge changes from topic1 down to master and delete topic1
git checkout master  > /dev/null 2>&1
merge_branch topic1  > /dev/null
git branch -d topic1 > /dev/null

# Add some more commits
write_and_commit root_file.txt "root\nstill"

# Create topic2
git branch topic2 > /dev/null

# Add a commit on topic2
git checkout topic2 > /dev/null 2>&1
write_and_commit subdir1/file1.txt "simple change"

# Add a commit on master
git checkout master > /dev/null 2>&1
write_and_commit subdir2/file1.txt "some new change"

# Create topic3 from master
git branch topic3 > /dev/null

# Add another commit on master
write_and_commit root_file.txt "root"

# Add a commit on topic3
git checkout topic3 > /dev/null 2>&1
write_and_commit subdir3/file1.txt "new subdir"

# Merge changes from master up to topic2
git checkout topic2 > /dev/null 2>&1
merge_branch master

# Merge changes from master up to topic3
git checkout topic3 > /dev/null 2>&1
merge_branch master

# Add new commit on master
git checkout master > /dev/null 2>&1
write_and_commit root_file.txt "yet another change"

# Merge topic 3 back
merge_branch topic3

#
# Now finally output the example.
#
set -v
git branch


git log --format=oneline --abbrev-commit --date-order


git-compare-branch master topic3


git-compare-branch master topic1 --pretty


git-compare-branch master topic1 --both-ways --pretty --summary --commits --finger --graph


git-compare-branch master topic1 --both-ways --pretty --summary --commits --finger --graph --exclude-updates
set +v


#
# Clean up the repo.
#
cd - > /dev/null
rm -fr "$REPONAME"
