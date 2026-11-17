FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm make python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY build-requirements.lock /work/
# pglast 8.8 sdist: the Cython-generated pglast/parser.c and a vendored libpg_query 18.1.0 (PostgreSQL 18.6 parser).
# The bison/flex outputs carry #line directives to gram.y and scan.l, which are not shipped; they are removed
# so LLVM coverage is attributed to the pinned C files.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/62/b2/fa8b837b58f352e5941ea7a8160121d32bad978a55538232d7890b8aaad5/pglast-8.8.tar.gz --output /work/pglast.tar.gz \
    && echo 'ff9998ec6bac4f30f84db6b6edb28a0fb03b1eda5c8ad211ab8362f5a08b833b  /work/pglast.tar.gz' | sha256sum --check \
    && mkdir /work/pglast-source \
    && tar -xzf /work/pglast.tar.gz -C /work/pglast-source --strip-components=1 \
    && cd /work/pglast-source \
    && printf '%s\n' \
       'e524ba6ff8c5bed3b0a9852bc2be78c44ac36c2c2563b2a032a897b7dff070d5  pglast/parser.c' \
       '31e4e51554e858cded7d162c4f1a093855293b57143bcdbf14a1c53cfc7f1338  libpg_query/src/postgres/src_backend_parser_gram.c' \
       'f9352c20940619a380a5e9f23cebe34d8f797cfbd747fc236a7a3e5fc8ef9b41  libpg_query/LICENSE' \
       | sha256sum --check \
    && grep -qx 'license = "GPL-3.0-or-later"' pyproject.toml \
    && grep -qx 'VERSION = 18.1.0' libpg_query/Makefile \
    && sed -i '/^#line /d' libpg_query/src/postgres/src_backend_parser_gram.c libpg_query/src/postgres/src_backend_parser_scan.c
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# libpg_query is built first with LLVM source coverage; setup.py's own "make build" then finds it up to date.
RUN cd /work/pglast-source/libpg_query \
    && make -j"$(nproc)" CC=clang CFLAGS='-fprofile-instr-generate -fcoverage-mapping' build \
    && cd /work/pglast-source \
    && CC=clang LDSHARED='clang -shared' \
       CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' \
       /opt/venv/bin/pip install --no-build-isolation --no-deps . \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import pglast; assert pglast.__version__ == "v8.8", pglast.__version__; print(pglast.parse_sql("SELECT 1"))'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; /opt/venv/bin/pip show pglast setuptools | grep -E '^(Name|Version):'; echo 'libpg_query 18.1.0 (vendored in the pglast 8.8 sdist; PostgreSQL 18.6 parser sources)'; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-pglast-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/pglast-source /work/pglast-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
