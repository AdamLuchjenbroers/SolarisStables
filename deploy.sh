#!/bin/sh

# Script to perform SVN export and set permissions correctly
svn export http://192.168.7.50/svn/solaris ./ --force
svn export http://192.168.7.50/svn/solaris/static /var/www/static/ --force

rm -rf static
chown wwwrun:www * /var/www/static -R

chmod ug+x solaris.wsgi
chmod ug+x deploy.sh

for file in `find . | grep py$`; do
  chmod ug+x $file
done
