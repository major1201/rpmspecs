# How to build?

## Download sources

```bash
wget -O SOURCES/linux-4.4.76.tar.xz https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.4.76.tar.xz
```

## Build

For EL6

```bash
docker run --rm \
    -v "$PWD/SOURCES":/root/rpmbuild/SOURCES:ro \
    -v "$PWD/SPECS":/root/rpmbuild/SPECS:ro \
    -v "$PWD/RPMS":/root/rpmbuild/RPMS \
    major1201/rpmbuild:6 \
    SPECS/kernel-lt-4.4.spec
```

For EL7

```bash
docker run --rm \
    -v "$PWD/SOURCES":/root/rpmbuild/SOURCES:ro \
    -v "$PWD/SPECS":/root/rpmbuild/SPECS:ro \
    -v "$PWD/RPMS":/root/rpmbuild/RPMS \
    major1201/rpmbuild:7 \
    SPECS/kernel-lt-4.4.spec
```
