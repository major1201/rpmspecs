# How to build?

## Download sources

```bash
wget -O SOURCES/php-5.6.15.tar.gz https://www.php.net/distributions/php-5.6.15.tar.gz
wget -O SOURCES/zend-loader-php5.6-linux-x86_64.tar.gz http://downloads.zend.com/guard/7.0.0/zend-loader-php5.6-linux-x86_64.tar.gz
```

## Build

For EL6

```bash
docker run --rm \
    -v "$PWD/SOURCES":/root/rpmbuild/SOURCES:ro \
    -v "$PWD/SPECS":/root/rpmbuild/SPECS:ro \
    -v "$PWD/RPMS":/root/rpmbuild/RPMS \
    major1201/rpmbuild:6 \
    SPECS/php6.spec
```

For EL7

```bash
docker run --rm \
    -v "$PWD/SOURCES":/root/rpmbuild/SOURCES:ro \
    -v "$PWD/SPECS":/root/rpmbuild/SPECS:ro \
    -v "$PWD/RPMS":/root/rpmbuild/RPMS \
    major1201/rpmbuild:7 \
    SPECS/php7.spec
```
