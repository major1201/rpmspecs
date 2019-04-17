Name:           proxychains-ng
Version:        4.12
Release:        1%{?dist}
Summary:        proxychains-ng by @major1201

License:        GPL-2.0
URL:            https://github.com/rofl0r/proxychains-ng
Source0:        proxychains-ng-4.12.tar.xz

BuildRequires:  gcc,gcc-c++,autoconf


%description
ProxyChains is a UNIX program, that hooks network-related libc functions
in DYNAMICALLY LINKED programs via a preloaded DLL (dlsym(), LD_PRELOAD)
and redirects the connections through SOCKS4a/5 or HTTP proxies.
It supports TCP only (no UDP/ICMP etc).


%prep
%setup -T -b 0 -n proxychains-ng-%{version}


%build
./configure --prefix=/usr --sysconfdir=/etc
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install
make install-config DESTDIR=%{?buildroot}


%clean
rm -rf $RPM_BUILD_ROOT


%files
/usr/bin/proxychains4
/usr/lib/libproxychains4.so
%config(noreplace) /etc/proxychains.conf
