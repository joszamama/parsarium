FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-14-dev llvm python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# pytomlpp 1.1.0 sdist: src/*.cpp and include/pytomlpp are the pybind11 module; third_party/tomlplusplus
# is the toml++ submodule at commit e7aaccca (the pytomlpp v1.1.0 tag), a snapshot after the v3.4.0 release.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/10/fe/50ca1ac0c1a932d3e71311baff531c0395e546ec0cd42bc8a8a88c36e00b/pytomlpp-1.1.0.tar.gz --output /work/pytomlpp.tar.gz \
    && echo '61a0f73e7ba2fe8bba4e99ce6d2701491885850b53aad8f3e46d03c4b31e594d  /work/pytomlpp.tar.gz' | sha256sum --check \
    && mkdir /work/pytomlpp-source \
    && tar -xzf /work/pytomlpp.tar.gz --strip-components=1 -C /work/pytomlpp-source \
    && cd /work/pytomlpp-source \
    && printf '%s\n' \
       'fe5ab8a244ffef62bd68566ec727c7cc511e713c5eddcfbc08602e53e6d57224  src/pytomlpp.cpp' \
       '50f3b593c19fb28fa9f7b6436ceb5cab686f4cb1adf7e11e845eb3f24c152492  src/type_casters.cpp' \
       '69cebd8759546840bc9f3627e62d8f286d68baa8238ca618507f50e934879211  src/encoding_decoding.cpp' \
       'ecff3b55f0e28d636b0d6144ae3d2e0d34beb9362cd9e3e439a6b43a2307e02d  src/pytomlpp/_io.py' \
       '92432152c9484708206269e915a4f3e53d49a25c9ebaebeff8a16359f0ed6379  include/pytomlpp/pytomlpp.hpp' \
       '556f60d4a1e9678fdd0d3fc9af2d5d20945ff23f7e2d0ca497a4ad488ba3eb5e  third_party/tomlplusplus/include/toml++/impl/parser.inl' \
       '3685f81a5d1a3c520790890888d6fb4b6846a42e7e5467a522a01973389ee169  LICENSE' \
       '529bc3900a9571e49db285b0df432397e70b881cc3bf48de6667ae74ff4b06d8  third_party/tomlplusplus/LICENSE' \
       | sha256sum --check \
    && grep -Fx 'Version: 1.1.0' PKG-INFO \
    && grep -F 'License :: OSI Approved :: MIT License' setup.cfg
COPY build-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# Every translation unit carries LLVM coverage mapping; the merge step keeps only the vendored toml++
# headers as parser source and counts pytomlpp's own sources as wrapper lines.
RUN cd /work/pytomlpp-source \
    && CC=clang CXX=clang++ LDSHARED='clang++ -shared' \
       CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       CXXFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' \
       /opt/venv/bin/pip install --use-pep517 --no-build-isolation --no-deps --no-index . \
    && diff -r --exclude=__pycache__ --exclude='_impl*.so' /work/pytomlpp-source/src/pytomlpp /opt/venv/lib/python3.11/site-packages/pytomlpp \
    && cd /tmp \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import pytomlpp; from importlib.metadata import version; assert version("pytomlpp") == "1.1.0"; assert pytomlpp.lib_version == "3.4.0", pytomlpp.lib_version; print(pytomlpp.loads("ready = true\n"))'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; \
      /opt/venv/bin/pip show pytomlpp pybind11 setuptools | grep -E '^(Name|Version):'; \
      echo 'toml++ submodule e7aaccca3fa3dbde9818ab8313250f3da4976e37 (lib_version 3.4.0)'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-pytomlpp-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/pytomlpp-source /work/pytomlpp-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY expected /work/expected
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
