# How to build?

## Download sources

```bash
wget -O SOURCES/mysql-5.7.17.tar.gz https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.17.tar.gz
wget -O SOURCES/boost_1_59_0.tar.gz https://jaist.dl.sourceforge.net/project/boost/boost/1.59.0/boost_1_59_0.tar.gz
```

## Build

For EL6

```bash
docker run --rm \
    -v "$PWD/SOURCES":/root/rpmbuild/SOURCES:ro \
    -v "$PWD/SPECS":/root/rpmbuild/SPECS:ro \
    -v "$PWD/RPMS":/root/rpmbuild/RPMS \
    major1201/rpmbuild:6 \
    SPECS/mysql6.spec
```

For EL7

```bash
docker run --rm \
    -v "$PWD/SOURCES":/root/rpmbuild/SOURCES:ro \
    -v "$PWD/SPECS":/root/rpmbuild/SPECS:ro \
    -v "$PWD/RPMS":/root/rpmbuild/RPMS \
    major1201/rpmbuild:7 \
    SPECS/mysql7.spec
```
