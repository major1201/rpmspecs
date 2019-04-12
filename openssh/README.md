# How to build?

## Download sources

```bash
wget -O SOURCES/openssh-7.5p1.tar.gz https://cloudflare.cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-7.5p1.tar.gz
```

## Build

For EL6

```bash
docker run --rm \
    -v "$PWD/SOURCES":/root/rpmbuild/SOURCES:ro \
    -v "$PWD/SPECS":/root/rpmbuild/SPECS:ro \
    -v "$PWD/RPMS":/root/rpmbuild/RPMS \
    major1201/rpmbuild:6 \
    SPECS/openssh6.spec
```

For EL7

```bash
docker run --rm \
    -v "$PWD/SOURCES":/root/rpmbuild/SOURCES:ro \
    -v "$PWD/SPECS":/root/rpmbuild/SPECS:ro \
    -v "$PWD/RPMS":/root/rpmbuild/RPMS \
    major1201/rpmbuild:7 \
    SPECS/openssh7.spec
```
