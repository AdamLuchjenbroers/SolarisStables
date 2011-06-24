#!/bin/sh

# Script to perform SVN export and set permissions correctly
svn export http://192.168.7.50/svn/solaris ./ --force

chown wwwrun:www * -R

for file in `find . | grep py$`; do
  chmod ug+x $file
done
