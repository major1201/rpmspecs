Name:           php-pecl-memcache
Version:        3.0.8
Release:        1%{?dist}
Summary:        PHP extension for interfacing with memcached via libmemcached library by @major1201

License:        PHP
URL:            https://pecl.php.net/package/memcache
Source0:        memcache-3.0.8.tgz
Source1:        005-memcache.ini

BuildRequires:  php
Requires:       php

%description
This extension uses libmemcached library to provide API for communicating with memcached servers.


%prep
%setup -c -b 0


%build
cd ../memcache-3.0.8
/usr/local/php/bin/phpize
./configure --with-php-config=/usr/local/php/bin/php-config
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd ../memcache-3.0.8
make install INSTALL_ROOT=$RPM_BUILD_ROOT
install -p -D -m 0644 %{SOURCE1} %{buildroot}/usr/local/php/conf.d/005-memcache.ini


%clean
rm -rf $RPM_BUILD_ROOT


%files
/usr/local/php
