xenserver-core
==============

Buildroot for xen-api and related packages, producing RPM and (experimentally) Debian packages.

RPM-based distributions
-----------------------

On RPM-based distributions, the packages are build using `mock`.   
To install it on a RHEL/CentOS system then you will need to add the
[EPEL repositories](http://fedoraproject.org/wiki/EPEL). 
Here is a useful article for [CentOS](http://www.rackspace.com/knowledge_center/article/installing-rhel-epel-repo-on-centos-5x-or-6x).


After adding EPEL, install and set up mock:

```
yum install -y mock redhat-lsb-core
```

Mock will refuse to run as root. You must choose a non-privileged user to
run mock as. Type the following as root:

(Note select a `<user>` which isn't "mock" when typing the commands below)

```
useradd <user> -G mock
passwd <user>

su - <user>
```

You are now ready to clone the xenserver-core repository and build the packages:

```
git clone git://github.com/xapi-project/xenserver-core.git

cd xenserver-core

./configure.sh

./makemake.py > Makefile

make
```
