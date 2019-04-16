Name:           php-pecl-redis
Version:        3.1.2
Release:        1%{?dist}
Summary:        PHP extension for interfacing with Redis by @major1201

License:        PHP
URL:            https://pecl.php.net/package/redis
Source0:        redis-3.1.2.tgz
Source1:        007-redis.ini

BuildRequires:  php
Requires:       php

%description
This extension provides an API for communicating with Redis servers.


%prep
%setup -c -b 0


%build
cd redis-3.1.2
/usr/local/php/bin/phpize
./configure --with-php-config=/usr/local/php/bin/php-config
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd redis-3.1.2
make install INSTALL_ROOT=$RPM_BUILD_ROOT
install -p -D -m 0644 %{SOURCE1} %{buildroot}/usr/local/php/conf.d/007-redis.ini


%clean
rm -rf $RPM_BUILD_ROOT


%files
/usr/local/php
