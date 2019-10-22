git describe --tags | awk "{split(\$0,a,\"-\"); print a[1];}" > version.tmp

# Only proceed if version number has actually changed (i.e. a new tag has been created)
if [ ! $(cmp --silent version.tmp version.txt) ]
then
    NEWVER=$(cat version.txt)
    echo Adding tag $NEWVER
    git tag -a $NEWVER -m ''
    rm version.tmp
fi