#!/bin/sh

# Script to perform SVN export and set permissions correctly
git pull

#rm -rf static
chown apache:apache * /var/www/static -R

chmod ug+x solaris.wsgi
chmod ug+x deploy.sh

for file in `find . | grep py$`; do
  chmod ug+x $file
done
