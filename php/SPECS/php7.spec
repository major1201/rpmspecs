Name:           php
Version:        5.6.15
Release:        1%{?dist}
Summary:        Php by @major1201

License:        PHP and Zend and BSD
URL:            http://www.php.net/
Source0:        php-5.6.15.tar.gz
Source1:        php-fpm.service

BuildRequires:  gcc,gcc-c++,libmcrypt-devel mhash-devel libxslt-devel libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel zlib zlib-devel glibc glibc-devel glib2 glib2-devel bzip2 bzip2-devel ncurses ncurses-devel curl curl-devel e2fsprogs e2fsprogs-devel krb5-devel libidn libidn-devel openssl openssl-devel
Requires:       libmcrypt-devel mhash-devel libxslt-devel libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel libxml2 libxml2-devel zlib zlib-devel glibc glibc-devel glib2 glib2-devel bzip2 bzip2-devel ncurses ncurses-devel curl curl-devel e2fsprogs e2fsprogs-devel krb5-devel libidn libidn-devel openssl openssl-devel

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts. 


%prep
%setup -T -b 0


%build
./configure \
--prefix=/usr/local/php \
--enable-fpm \
--with-fpm-user=www \
--with-fpm-group=www \
--with-mcrypt \
--enable-mbstring \
--disable-pdo \
--with-curl \
--disable-debug \
--disable-rpath \
--enable-inline-optimization \
--with-bz2 \
--with-zlib \
--enable-sockets \
--enable-sysvsem \
--enable-sysvshm \
--enable-pcntl \
--enable-mbregex \
--with-mhash \
--enable-zip \
--with-pcre-regex \
--with-mysql \
--with-mysqli \
--with-gd \
--with-jpeg-dir
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/php-fpm.service
# remove additional files
rm -rf %{buildroot}/.channels %{buildroot}/.depdb %{buildroot}/.depdblock %{buildroot}/.filemap %{buildroot}/.lock
\cp -f %{buildroot}/usr/local/php/etc/php-fpm.conf.default %{buildroot}/usr/local/php/etc/php-fpm.conf


%clean
rm -rf $RPM_BUILD_ROOT


%pre
groupadd www
id www || useradd -s /sbin/nologin -g www www


%post
/usr/bin/systemctl daemon-reload


%preun
%systemd_preun php-fpm.service


%postun
%systemd_postun php-fpm.service
if [ $1 -eq 0 ]; then
  /usr/bin/rm -rf /usr/local/php
fi


%files
#%doc
/usr/local/php
%{_unitdir}/php-fpm.service
