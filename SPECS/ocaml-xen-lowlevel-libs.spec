Name:           ocaml-xen-lowlevel-libs
Version:        0.9.10
Release:        3
Summary:        Xen hypercall bindings for OCaml
License:        LGPL
Group:          Development/Other
URL:            https://github.com/xapi-project/ocaml-xen-lowlevel-libs/archive/ocaml-xen-lowlevel-libs-%{version}.tar.gz
Source0:        https://github.com/xapi-project/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml ocaml-findlib ocaml-camlp4-devel ocaml-ocamldoc
BuildRequires:  ocaml-lwt-devel xen-devel libuuid-devel cmdliner-devel 
BuildRequires:  ocaml-cstruct-devel
Requires:       ocaml ocaml-findlib

%description
Xen hypercall bindings for OCaml.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other
#Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q

%build
make configure
./configure --disable-xenctrl
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}/ocaml
mkdir -p %{buildroot}/%{_libdir}/ocaml/stublibs
export OCAMLFIND_DESTDIR=%{buildroot}/%{_libdir}/ocaml
export OCAMLFIND_LDCONF=ignore
make install DESTDIR=${buildroot}

%clean
rm -rf %{buildroot}

%files
#This space intentionally left blank

%files devel
%defattr(-,root,root)
%doc README.md
%{_libdir}/ocaml/xenlight/*
%{_libdir}/ocaml/stublibs/dllxenlight_stubs.so
%{_libdir}/ocaml/stublibs/dllxenlight_stubs.so.owner
%{_libdir}/ocaml/stublibs/dllxentoollog_stubs.so
%{_libdir}/ocaml/stublibs/dllxentoollog_stubs.so.owner

%changelog
* Mon Oct 21 2013 Jon Ludlam <jonathan.ludlam@eu.citrix.com>
- Reinstate xenlight, remove xenctrl

* Sun Oct 20 2013 David Scott <dave.scott@eu.citrix.com>
- Remove xenlight because this old version isn't enough for xenopsd-xenlight

* Mon Sep 16 2013 Euan Harris <euan.harris@citrix.com>
- Update to 0.9.9, which includes linker paths required on Debian

* Fri Jun 21 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.2

* Tue Jun 18 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.1

* Mon Jun  3 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package

