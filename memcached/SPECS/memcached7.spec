Name:           memcached
Version:        1.4.36
Release:        1%{?dist}
Summary:        High Performance, Distributed Memory Object Cache by @major1201

Group:          System Environment/Daemons
License:        BSD
URL:            http://memcached.org
Source0:        %{name}-1.4.36.tar.gz
Source1:        memcached.service

BuildRequires:  libevent-devel

%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.

%prep
%setup -T -b 0


%build
./configure --prefix=/usr/local/memcached

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# remove memcached-debug
rm -f %{buildroot}/%{_bindir}/memcached-debug

# Perl script for monitoring memcached
install -Dp -m0755 scripts/memcached-tool %{buildroot}/usr/local/memcached/bin/memcached-tool

# Init script
install -Dp -m0755 %{SOURCE1} %{buildroot}%{_unitdir}/memcached.service

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
/usr/bin/systemctl daemon-reload

%preun
%systemd_preun memcahced.service

%postun
%systemd_postun memcahced.service
if [ $1 -eq 0 ]; then
  /usr/bin/rm -rf /usr/local/memcahced
fi


%files
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/memcached.service
/usr/local/memcached/
