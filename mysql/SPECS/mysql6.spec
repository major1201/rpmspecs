Name:           mysql
Version:        5.7.17
Release:        1%{?dist}
Summary:        Mysql Database my @major1201

License:        BSD
URL:            http://www.mysql.com
Source0:        mysql-5.7.17.tar.gz
Source1:        boost_1_59_0.tar.gz
Source2:        mysqld.sh
Source3:        my.cnf

BuildRequires:  gcc,gcc-c++
BuildRequires:  cmake >= 2.8.2
BuildRequires:  perl,perl-Time-HiRes,time,libaio-devel,ncurses-devel,numactl-devel,openssl-devel,zlib-devel
Requires:       coreutils,grep,procps,shadow-utils,net-tools,numactl-devel
AutoReq:        no


%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server.


%prep
%setup -q -T -b 0 -b 1


%build
cmake \
-DBUILD_CONFIG=mysql_release \
-DINSTALL_LAYOUT=RPM \
-DCMAKE_INSTALL_PREFIX=/usr/local/mysql \
-DMYSQL_DATADIR=/var/mysql/data \
-DEXTRA_CHARSETS=all \
-DDEFAULT_CHARSET=utf8mb4 \
-DDEFAULT_COLLATION=utf8mb4_general_ci \
-DMYSQL_TCP_PORT=3306 \
-DMYSQL_USER=mysql \
-DWITH_MYISAM_STORAGE_ENGINE=1 \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_ARCHIVE_STORAGE_ENGINE=1 \
-DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
-DWITH_PARTITION_STORAGE_ENGINE=1 \
-DWITH_FEDERATED_STORAGE_ENGINE=1 \
-DWITH_MEMORY_STORAGE_ENGINE=1 \
-DWITH_EMBEDDED_SERVER=1 \
-DENABLED_LOCAL_INFILE=1 \
-DWITH_BOOST=..
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%make_install
install -p -D -m 0755 %{SOURCE2} %{buildroot}/etc/init.d/mysqld
install -p -D -m 0644 %{SOURCE3} %{buildroot}/usr/local/mysql/share/mysql/my.cnf


%clean
rm -rf $RPM_BUILD_ROOT


%pre
if [ $1 -eq 1 ]; then
  mkdir -p /var/mysql/data
  groupadd mysql
  id mysql || useradd -g mysql -d /var/mysql mysql
  chown -R mysql:mysql /var/mysql/

  mkdir -p /var/lib/mysql-files/
  chown mysql:mysql /var/lib/mysql-files/
fi


%post
if [ $1 -eq 1 ]; then
  chown -R mysql:mysql /usr/local/mysql/
  \cp -f /usr/local/mysql/share/mysql/my.cnf /etc/my.cnf
  /usr/local/mysql/sbin/mysqld --initialize --user=mysql --explicit_defaults_for_timestamp &>> /var/mysql/initialize.log
  chown -R mysql:mysql /usr/lib64/mysql/
fi


%preun
/etc/init.d/mysqld stop


%postun
if [ $1 -eq 0 ]; then
  /bin/rm -rf /usr/local/mysql
  /bin/rm -f /etc/init.d/mysqld
fi


%files
/usr/local/mysql/*
/etc/init.d/mysqld
