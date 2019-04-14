# How to build?

## Download sources

```bash
wget -O SOURCES/openvswitch-2.5.2.tar.gz https://www.openvswitch.org/releases/openvswitch-2.5.2.tar.gz
```

## Build

For EL6

```bash
docker run --rm \
    -v "$PWD/SOURCES":/root/rpmbuild/SOURCES:ro \
    -v "$PWD/SPECS":/root/rpmbuild/SPECS:ro \
    -v "$PWD/RPMS":/root/rpmbuild/RPMS \
    major1201/rpmbuild:6 \
    --nocheck SPECS/openvswitch_no_kmod.spec
```

For EL7

```bash
docker run --rm \
    -v "$PWD/SOURCES":/root/rpmbuild/SOURCES:ro \
    -v "$PWD/SPECS":/root/rpmbuild/SPECS:ro \
    -v "$PWD/RPMS":/root/rpmbuild/RPMS \
    major1201/rpmbuild:7 \
    --nocheck SPECS/openvswitch_no_kmod.spec
```
