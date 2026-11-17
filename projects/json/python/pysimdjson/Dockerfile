FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl clang libclang-rt-14-dev libstdc++-12-dev llvm python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY build-requirements.lock /work/
# pysimdjson 8.0.0 sdist; it vendors the simdjson 5.1.1 single-header amalgamation under simdjson/.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/51/ef/0af5d4a9f2f8440d0bff7a109639edc5b19cff9e1062cab55ff51c586d9c/pysimdjson-8.0.0.tar.gz -o /work/pysimdjson.tar.gz \
    && echo 'e5669f38c3d91017361d708654c5a58130a91102dd56f001bfa4dc0f923edd00  /work/pysimdjson.tar.gz' | sha256sum --check \
    && mkdir -p /work/pysimdjson-source \
    && tar -xzf /work/pysimdjson.tar.gz -C /work/pysimdjson-source --strip-components=1 \
    && cd /work/pysimdjson-source \
    && printf '%s\n' \
       '3b1d9c47fc7dd5942ee540a2bbdb510dfe912cb187f814071744c7e020bb04d6  simdjson/csimdjson.pyx' \
       '05aba2fdf75acbe779e41b6eaff16f52c92efae6d7458f058aced9dc6fc47585  simdjson/csimdjson.pxd' \
       '87da530837ba1677ae9f522ce427d46304fcc5dc91a427a294d183560e39f061  simdjson/util.cpp' \
       '02ff0e9510846b7220060e3e555160bb26efdbd200c8fe31d79bec8b5f37374e  simdjson/util.h' \
       '3fbca3e4846e0fe5cdb3d89739af41c1289200afae4ccd931ccbc68116d4d040  simdjson/ondemand.h' \
       '3ea5f501cef6c2e16e28095b566feeb56021ca473aaf50aad32102f45d734195  simdjson/simdjson.cpp' \
       'f3e5ee5f39051960b5ce65762ee4b6919caf270675eb52240ebd92f21a5bcefd  simdjson/simdjson.h' \
       '667ed560f1621e0c930e864b20b82de7a00c1a21bbe23e0fa2921bfec2f5d0de  simdjson/__init__.py' \
       '0da183662a0134294ae49d3627f554cea11203425dd096e451c5dbdf2cb496ef  pyproject.toml' \
       '1067c30a692a52f66c3b8c1bd6df26efdd7d84a43ef8ebe10ccb395f7e79ddec  LICENSE' \
       | sha256sum --check
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# The sdist ships no generated C++; Cython 3.3.1 writes simdjson/csimdjson.cpp in the source tree.
RUN cd /work/pysimdjson-source \
    && CC=clang CXX=clang++ LDSHARED='clang++ -shared' LDCXXSHARED='clang++ -shared' \
       CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       CXXFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' \
       /opt/venv/bin/pip install --no-build-isolation --no-deps . \
    && test -f /work/pysimdjson-source/simdjson/csimdjson.cpp \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import simdjson; assert simdjson.VERSION == "5.1.1", simdjson.VERSION; p = simdjson.Parser(); print(p.implementation, p.parse(b"{\"ready\":true}", True))'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; /opt/venv/bin/pip show pysimdjson setuptools cython | grep -E '^(Name|Version):'; echo 'simdjson 5.1.1 (amalgamation vendored in the pysimdjson 8.0.0 sdist)'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-pysimdjson-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/pysimdjson-source /work/pysimdjson-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
