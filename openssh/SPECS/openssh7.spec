# OpenSSH privilege separation requires a user & group ID
%define sshd_uid    74
%define sshd_gid    74

Name:           openssh
Version:        7.5p1
Release:        1%{?dist}
Summary:        An open source implementation of SSH protocol versions 1 and 2 @major1201

License:        BSD
URL:            http://www.openssh.com/portable.html
Source0:        openssh-7.5p1.tar.gz
Source1:        sshd7.pam
Source2:        sshd@.service
Source3:        sshd.socket
Source4:        sshd.service
Source5:        sshd_config
Source6:        sshd-keygen.service
Source7:        sshd.sysconfig
Source8:        sshd-keygen

BuildRequires:  perl,openssl-devel,/bin/login,pam,pam-devel,openldap-devel
Requires:       initscripts >= 5.20,chkconfig >= 0.9

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
	--with-systemd \
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
install -p -D -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/sshd@.service
install -p -D -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/sshd.socket
install -p -D -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/sshd.service
install -p -D -m644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/ssh/sshd_config
install -p -D -m644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/sshd-keygen.service
install -p -D -m644 %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/sshd
install -p -D -m755 %{SOURCE8} $RPM_BUILD_ROOT/%{_sbindir}/sshd-keygen
install -p -D -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*


%clean
rm -rf $RPM_BUILD_ROOT


%pre
getent group sshd >/dev/null || groupadd -g %{sshd_uid} -r sshd || :
getent passwd sshd >/dev/null || \
  useradd -c "Privilege-separated SSH" -u %{sshd_uid} -g sshd \
  -s /sbin/nologin -r -d /var/empty/sshd sshd 2> /dev/null || :


%post
%systemd_post sshd.service sshd.socket


%preun
%systemd_preun sshd.service sshd.socket


%postun
%systemd_postun_with_restart sshd.service


%files
%config %{_sysconfdir}/ssh
%config %{_unitdir}/sshd@.service
%config %{_unitdir}/sshd.socket
%config %{_unitdir}/sshd.service
%config %{_unitdir}/sshd-keygen.service
%attr(0644,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0640,root,root) %config(noreplace) /etc/sysconfig/sshd

%{_sbindir}/sshd
%{_sbindir}/sshd-keygen
%{_libexecdir}/openssh/*
%{_bindir}/*

%{_mandir}
%dir %{_var}/empty/sshd
