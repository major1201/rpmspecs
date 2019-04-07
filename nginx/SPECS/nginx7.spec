Name:           nginx
Version:        1.10.1
Release:        1%{?dist}
Summary:        Nginx web server my @major1201

License:        BSD
URL:            http://nginx.org
Source0:        https://nginx.org/download/nginx-1.10.1.tar.gz
Source1:        nginx.service

BuildRequires:  gcc,gcc-c++,openssl,openssl-devel,pcre-devel,pcre
Requires:       openssl,openssl-devel,pcre-devel,pcre

%description
Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and
IMAP protocols, with a strong focus on high concurrency, performance and low
memory usage. This package is built by @major1201.


%prep
%setup -T -b 0


%build
./configure \
--user=nginx \
--group=nginx \
--prefix=/usr/local/nginx \
--pid-path=/var/run/nginx.pid \
--with-http_stub_status_module \
--with-http_ssl_module \
--with-http_v2_module \
--with-http_gzip_static_module \
--with-ipv6 \
--with-http_sub_module
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/nginx.service


%clean
rm -rf $RPM_BUILD_ROOT


%pre
groupadd nginx
id nginx || useradd -s /sbin/nologin -g nginx nginx


%post
/usr/bin/systemctl daemon-reload


%preun
%systemd_preun nginx.service


%postun
%systemd_postun nginx.service
if [ $1 -eq 0 ]; then
  /usr/bin/rm -rf /usr/local/nginx
fi


%files
#%doc
/usr/local/nginx/*
%{_unitdir}/nginx.service

