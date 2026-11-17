FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# ruamel.yaml.clib 0.2.15 sdist: Cython-generated _ruamel_yaml.c plus its libyaml-derived C sources.
RUN mkdir /work/wheels /work/clib-src \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ea/97/60fda20e2fb54b83a61ae14648b0817c8f5d84a3821e40bfbdae1437026a/ruamel_yaml_clib-0.2.15.tar.gz --output /work/clib.tar.gz \
    && echo '46e4cc8c43ef6a94885f72512094e482114a8a706d3c555a34ed4b0d20200600  /work/clib.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b8/0c/51f6841f1d84f404f92463fc2b1ba0da357ca1e3db6b7fbda26956c3b82a/ruamel_yaml-0.19.1-py3-none-any.whl --output /work/wheels/ruamel_yaml-0.19.1-py3-none-any.whl \
    && echo '27592957fedf6e0b62f281e96effd28043345e0e66001f97683aa9a40c667c93  /work/wheels/ruamel_yaml-0.19.1-py3-none-any.whl' | sha256sum --check \
    && tar -xzf /work/clib.tar.gz --strip-components=1 -C /work/clib-src \
    && cd /work/clib-src \
    && printf '%s\n' \
       '3f4895cb0eb25684105cddb6fcef4d91014da82d5ca4589def044d1dbf23a546  _ruamel_yaml.c' \
       '83d401743b71b9f8bf154579b2b6d1a54aba7eab329fcac3ab5f9c56fc36d025  _ruamel_yaml.pyx' \
       '23b9aa5a56be19b79f7a23f2805587a9ebf165c1367ec5759ef87eca0851d76e  scanner.c' \
       'edc8762e97bc3bebfd406ba88165261b099eb0fe8af21e5e7a7d75a879825205  parser.c' \
       'c428a44b177391557bdf49177c1dc0216edf2a2bbe0e24ca2ef2725ef7f01e9d  reader.c' \
       'fa95d1236017cfef165d148ce2f72dc74540f5268732c4256fa1b6bb535dcee3  api.c' \
       'f8ad7efe71dde909f2d694f7dc69470d3dbe07c001c0b30c6bd9951e472077fa  LICENSE' \
       | sha256sum --check \
    && grep -Fx 'License: MIT' /work/clib-src/PKG-INFO
COPY build-requirements.lock runtime-requirements.lock profile-list.txt /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock
# The pinned sdist's own build with clang -O0 and LLVM source coverage; profile-list.txt keeps the
# Cython-generated _ruamel_yaml.c binding uninstrumented, so coverage covers the libyaml-derived C.
RUN cd /work/clib-src \
    && CC=clang LDSHARED='clang -shared' \
       CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fprofile-list=/work/profile-list.txt' \
       LDFLAGS='-fprofile-instr-generate' \
       /opt/venv/bin/pip install --no-build-isolation --no-deps --no-index . \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'from ruamel.yaml import YAML, __version__; import ruamel.yaml.main; from _ruamel_yaml import CParser; assert __version__ == "0.19.1"; y = YAML(typ="safe"); assert y.Parser is CParser is ruamel.yaml.main.CParser; print(y.load(b"ready: true"))'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; \
      /opt/venv/bin/pip show ruamel.yaml ruamel.yaml.clib setuptools | grep -E '^(Name|Version):'; \
      cd /work/clib-src && sha256sum scanner.c parser.c reader.c api.c _ruamel_yaml.c; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-ruamel-clib-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/clib-src /work/clib-src
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh expected.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
