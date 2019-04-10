Name:           memcached
Version:        1.4.36
Release:        1%{?dist}
Summary:        High Performance, Distributed Memory Object Cache by @major1201

Group:          System Environment/Daemons
License:        BSD
URL:            http://memcached.org
Source0:        %{name}-1.4.36.tar.gz
Source1:        memcached.sysv

BuildRequires:  libevent-devel
BuildRequires:  perl(Test::More)
BuildRequires:  /usr/bin/prove
Requires: initscripts
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.

%prep
%setup -T -b 0


%build
./configure --prefix=/usr/local/memcached

make %{?_smp_mflags}

#%check
#make test

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# remove memcached-debug
rm -f %{buildroot}/%{_bindir}/memcached-debug

# Perl script for monitoring memcached
install -Dp -m0755 scripts/memcached-tool %{buildroot}/usr/local/memcached/bin/memcached-tool

# Init script
install -Dp -m0755 %{SOURCE1} %{buildroot}/etc/init.d/memcached

# Default configs
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cat <<EOF >%{buildroot}/%{_sysconfdir}/sysconfig/%{name}
PORT="11211"
USER="nobody"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
EOF

# make pid dir
mkdir -p %{buildroot}/usr/local/memcached/var/run/

%clean
rm -rf %{buildroot}


%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1
fi
exit 0


%files
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
/etc/init.d/memcached
/usr/local/memcached/
