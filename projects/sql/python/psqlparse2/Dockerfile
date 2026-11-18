FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
# Debian 12: Python 3.11 (psqlparse2 0.0.17 publishes cp38-cp312 wheels and pins Cython 3.0.10), clang 14.
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-14-dev llvm make python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY build-requirements.lock /work/
# psqlparse2 0.0.17 sdist: the Cython wrapper src/pg_query/__init__.py, the generated protobuf module
# src/psqlparse2/pb/pg_query_pb2.py and a vendored libpg_query 16-5.1.0 (PostgreSQL 16.1 parser).
# The bison/flex outputs carry #line directives to gram.y and scan.l, which are not shipped; they are
# removed so LLVM coverage is attributed to the pinned C files.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/cf/4e/0a642acfdc92ba7ab5a14c020d840dd57562d5f32ee41c647520dbea080f/psqlparse2-0.0.17.tar.gz --output /work/psqlparse2.tar.gz \
    && echo 'a2dc5674eb6300aa48fc236a013939c455d795ef5294b6994480c92781079443  /work/psqlparse2.tar.gz' | sha256sum --check \
    && mkdir /work/psqlparse2-source \
    && tar -xzf /work/psqlparse2.tar.gz -C /work/psqlparse2-source --strip-components=1 \
    && cd /work/psqlparse2-source \
    && printf '%s\n' \
       '266719c90e8b5174464d996b58a3f668710450d9d4449919af4e5b6deac14fa9  src/pg_query/__init__.py' \
       '23537e4c8d3be0425d985e30934cbaa7173e4502231a09dca96e109ed860f033  src/psqlparse2/__init__.py' \
       '3ec54ac01d16c52fa8fe4e7fe7871c73eed2babefc7691d4805fc8c14415e649  libpg_query/src/postgres/src_backend_parser_gram.c' \
       'fc47bbe6a19b737ddde033e45519f689616ad14c27a76f9539b35fd4941c5e2d  LICENSE' \
       'f9352c20940619a380a5e9f23cebe34d8f797cfbd747fc236a7a3e5fc8ef9b41  libpg_query/LICENSE' \
       | sha256sum --check \
    && grep -q 'License :: OSI Approved :: BSD License' pyproject.toml \
    && grep -qx 'VERSION = 5.1.0' libpg_query/Makefile \
    && grep -qx '#define PG_VERSION "16.1"' libpg_query/pg_query.h \
    && sed -i '/^#line /d' libpg_query/src/postgres/src_backend_parser_gram.c libpg_query/src/postgres/src_backend_parser_scan.c
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# setup.py's "generate" step runs libpg_query's own "make clean" and "make all" (DEBUG=1: -O0, its
# examples and C tests) and then Cython-compiles src/pg_query/__init__.py into an extension that links
# libpg_query.a statically. CC/CFLAGS put libpg_query and the Cython output under LLVM source coverage;
# the build-time C tests write their profiles to /dev/null.
RUN cd /work/psqlparse2-source \
    && CC=clang LDSHARED='clang -shared' \
       CFLAGS='-fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' TEST_LDFLAGS='-fprofile-instr-generate' \
       LLVM_PROFILE_FILE=/dev/null \
       /opt/venv/bin/pip install --no-build-isolation --no-deps . \
    && test -f /work/psqlparse2-source/src/pg_query/__init__.c \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import importlib.metadata as m, psqlparse2; assert m.version("psqlparse2") == "0.0.17", m.version("psqlparse2"); print(psqlparse2.query_to_pb("SELECT 1").version)'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; /opt/venv/bin/pip show psqlparse2 cython protobuf | grep -E '^(Name|Version):'; echo 'libpg_query 16-5.1.0 (vendored in the psqlparse2 0.0.17 sdist; PostgreSQL 16.1 parser sources)'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-psqlparse2-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/psqlparse2-source /work/psqlparse2-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
