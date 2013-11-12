#!/bin/sh

rm -rf dists
mkdir -p dists/saucy/main/binary-amd64
mkdir -p dists/saucy/main/binary-i386
mkdir -p dists/saucy/main/source

rsync --delete -avu SRPMS/* dists/saucy/main/source
rsync --delete -avu RPMS/*.deb dists/saucy/main/binary-amd64

cat >dists/saucy/main/binary-amd64/Release <<EOF
Archive: saucy
Version: 13.04
Component: main
Origin: Citrix
Label: XenServer Core
Architecture: amd64
EOF

cat >dists/saucy/main/source/Release <<EOF
Archive: saucy
Version: 13.04
Component: main
Origin: Citrix
Label: XenServer Core
Architecture: source
EOF

# Sometimes we get the wrong sizes in the packages file
# http://www.linuxquestions.org/questions/blog/bittner-195120/howto-build-your-own-debian-repository-2863/
#apt-ftparchive generate apt-saucy-release.conf
#apt-ftparchive -c apt-saucy-release.conf packages dists/saucy/main >dists/saucy/main/binary-amd64/Packages
#apt-ftparchive -c apt-saucy-release.conf release dists/saucy/ >dists/saucy/Release


# https://enc.com.au/2007/08/07/creating-an-apt-archive/
apt-ftparchive generate scripts/deb/archive.conf

echo "now run: rsync -avu --delete dists/ ~/public_html/dists/"
