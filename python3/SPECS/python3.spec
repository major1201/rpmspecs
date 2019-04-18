%if 0%{?fedora} || 0%{?rhel} >= 7
%global brp_python_hardlink /usr/lib/rpm/brp-python-hardlink
%else
%global brp_python_hardlink /usr/lib/rpm/redhat/brp-python-hardlink
%endif
%global __os_install_post /usr/lib/rpm/brp-compress \
  %{!?__debug_package:/usr/lib/rpm/brp-strip %{__strip}} \
  /usr/lib/rpm/brp-strip-static-archive %{__strip} \
  /usr/lib/rpm/brp-strip-comment-note %{__strip} %{__objdump} \
  %{brp_python_hardlink}


Name:           Python3
Version:        3.5.1
Release:        1%{?dist}
Summary:        python3.5 by @major1201

License:        Python
URL:            http://python.org
Source0:        Python-3.5.1.tar.xz

BuildRequires:  gcc,gcc-c++,autoconf,expat,zlib-devel,bzip2-devel,openssl-devel,ncurses-devel,sqlite-devel,readline-devel,tk-devel,gdbm-devel,db4-devel,libpcap-devel,xz-devel
Requires:       expat,zlib-devel,bzip2-devel,openssl-devel,ncurses-devel,sqlite-devel,readline-devel,tk-devel,gdbm-devel,db4-devel,libpcap-devel,xz-devel
AutoReq:        no


%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC). This package is built by @major1201.


%prep
%setup -T -b 0 -n Python-%{version}


%build
./configure \
--prefix=/usr/local/python3 \
--enable-shared
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install


%clean
rm -rf $RPM_BUILD_ROOT


%pre


%post
ln -sf /usr/local/python3/bin/python3 /usr/local/bin/python3
ln -sf /usr/local/python3/bin/pip3 /usr/local/bin/pip3
echo "/usr/local/python3/lib/" > /etc/ld.so.conf.d/python3.conf
ldconfig


%preun


%postun
if [ $1 -eq 0 ]; then
  rm -f /usr/local/bin/python3
  rm -f /usr/local/bin/pip3
  rm -f /etc/ld.so.conf.d/python3.conf
fi


%files
/usr/local/python3/*
