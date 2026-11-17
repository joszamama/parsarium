FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl clang libclang-rt-14-dev libstdc++-12-dev llvm python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY build-requirements.lock /work/
# ujson 6.1.0 sdist; it vendors double-conversion 3.2.0 under src/ujson/deps.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e0/60/ad782f70ce03d12ec23288292a17549ca537f9d188227340ac0d082421b3/ujson-6.1.0.tar.gz -o /work/ujson.tar.gz \
    && echo 'aef7ea4cd9e2e9f8a35c4538a9780d58c80d76c5da66a8dad269b4cc6d930c29  /work/ujson.tar.gz' | sha256sum --check \
    && mkdir -p /work/ujson-source \
    && tar -xzf /work/ujson.tar.gz -C /work/ujson-source --strip-components=1 \
    && cd /work/ujson-source \
    && printf '%s\n' \
       'c23c6c5a15666a6df182b0b827c9fedd676321027a45599af4f671272b464212  src/ujson/decode.c' \
       '566fa0e34113673a4aadbd2508c41df51ffa0ded4a79ed640acf9a42d3962873  src/ujson/ujson.c' \
       '09a7ae84bd102b3e5c8e60fb093202de081ac003e79986405a8db949a0b3c2e1  src/ujson/dconv_wrapper.cc' \
       '9aafd7e77a23164ee94903cfd16bd1e84344a5d7a18b4ee430e35e76568b108d  src/ujson/deps/double-conversion/double-conversion/string-to-double.cc' \
       '923f15ce6bff38b9aaa1f3bced157c468978ac9443fbb781f0826daeae5cd4ee  src/ujson/deps/double-conversion/double-conversion/strtod.cc' \
       '36866344f0a486541bd9800f1a407a056c0c214a82c658f059694daf3dc394d2  LICENSE.txt' \
       '4af93c12062c58058378de2397dc1c92bbff9ddfb1d583a01c84127557ce97ca  src/ujson/deps/double-conversion/LICENSE' \
       | sha256sum --check
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# UJSON_BUILD_NO_STRIP=1 is ujson's own switch to skip its Linux -Wl,--strip-all link flag.
RUN cd /work/ujson-source \
    && CC=clang CXX=clang++ LDSHARED='clang -shared' LDCXXSHARED='clang++ -shared' \
       CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       CXXFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' UJSON_BUILD_NO_STRIP=1 \
       /opt/venv/bin/pip install --no-build-isolation --no-deps . \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import ujson; assert ujson.__version__ == "6.1.0", ujson.__version__; print(ujson.loads(b"{\"ready\":true}"))'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; /opt/venv/bin/pip show ujson setuptools setuptools-scm | grep -E '^(Name|Version):'; echo 'double-conversion 3.2.0 (vendored in the ujson 6.1.0 sdist)'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-ujson-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/ujson-source /work/ujson-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
