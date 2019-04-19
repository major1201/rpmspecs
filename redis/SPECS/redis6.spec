Name:             redis
Version:          3.2.8
Release:          1%{?dist}
Summary:          A persistent key-value database by @major1201

Group:            Applications/Databases
License:          BSD
URL:              http://redis.io
Source0:          redis-3.2.8.tar.gz
Source1:          %{name}.init
Source2:          %{name}.logrotate
Source3:          %{name}.conf
Source4:          redis-shutdown

%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.

%prep
%setup -T -b 0

%build

%install
rm -fr %{buildroot}
make install PREFIX=%{buildroot}/usr/local/redis
# Install misc other
install -p -D -m 755 %{SOURCE1} %{buildroot}/etc/init.d/%{name}
install -p -D -m 644 %{SOURCE2} %{buildroot}/etc/logrotate.d/%{name}
install -d -m 755 %{buildroot}/usr/local/redis/etc/
install -p -D -m 644 %{SOURCE3} %{buildroot}/usr/local/redis/etc/%{name}.conf
install -p -D -m 755 %{SOURCE4} %{buildroot}/usr/local/redis/bin/redis-shutdown

%clean
rm -fr %{buildroot}

%pre
getent group redis &> /dev/null || groupadd -r redis &> /dev/null
getent passwd redis &> /dev/null || \
useradd -r -g redis -d %{_sharedstatedir}/redis -s /sbin/nologin -c 'Redis Server' redis &> /dev/null
mkdir -m 775 /var/run/redis /var/log/redis /var/redis
chown -R root:redis /var/run/redis
chown -R redis:redis /var/log/redis /var/redis
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/service redis stop &> /dev/null
fi

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/logrotate.d/%{name}
%config(noreplace) /usr/local/redis/etc/%{name}.conf
/etc/init.d/%{name}
/usr/local/redis/
