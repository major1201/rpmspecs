# OpenSSH privilege separation requires a user & group ID
%define sshd_uid    74
%define sshd_gid    74

%define _sysconfdir /etc

Name:           openssh
Version:        7.5p1
Release:        1%{?dist}
Summary:        An open source implementation of SSH protocol versions 1 and 2 @major1201

License:        BSD
URL:            http://www.openssh.com/portable.html
Source0:        openssh-7.5p1.tar.gz
Source1:        sshd6.pam
Source2:        sshd.init
Source3:        sshd_config

BuildRequires:  perl,openssl-devel,/bin/login,glibc-devel,pam,pam-devel,openldap-devel
Requires:       chkconfig >= 0.9,/etc/pam.d/system-auth

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features, as well as removing
all patented algorithms to separate libraries.

This package includes the core files necessary for both the OpenSSH
client and server. To make this package useful, you should also
install openssh-clients, openssh-server, or both.

This package is built by @major1201.

%prep
%setup -T -b 0


%build
%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--datadir=%{_datadir}/openssh \
	--with-default-path=/usr/local/bin:/bin:/usr/bin \
	--with-superuser-path=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin \
	--with-privsep-path=%{_var}/empty/sshd \
	--with-md5-passwords \
	--disable-strip \
	--without-zlib-version-check \
	--with-ssl-engine \
	--with-ipaddr-display \
	--with-pie=no \
	--with-pam \
	--with-ldap
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_var}/empty/sshd

%make_install

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
install -m644 %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m755 %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/sshd
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/ssh/sshd_config

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*


%clean
rm -rf $RPM_BUILD_ROOT


%pre
%{_sbindir}/groupadd -r -g %{sshd_gid} sshd 2>/dev/null || :
%{_sbindir}/useradd -d /var/empty/sshd -s /bin/false -u %{sshd_uid} \
	-g sshd -M -r sshd 2>/dev/null || :


%post
/sbin/chkconfig --add sshd


%postun
/sbin/service sshd condrestart > /dev/null 2>&1 || :


%preun
if [ "$1" = 0 ]
then
	/sbin/service sshd stop > /dev/null 2>&1 || :
	/sbin/chkconfig --del sshd
fi


%files
%config %{_sysconfdir}/ssh
%config /etc/rc.d/init.d/sshd
%config(noreplace) /etc/pam.d/sshd

%{_sbindir}/sshd
%{_libexecdir}/openssh/*
%{_bindir}/*

%{_mandir}
%dir %{_var}/empty/sshd
