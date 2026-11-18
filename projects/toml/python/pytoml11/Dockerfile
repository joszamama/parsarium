FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang-16 cmake curl libclang-rt-16-dev llvm-16 make python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# pytoml11 0.0.5 sdist: src/pytoml11.cpp is the pybind11 module; src/toml.hpp is the vendored single-header
# toml11 4.2.0 (TOML11_VERSION 4.2.0), the parser.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/5c/9f/dc10a6e1a64e54e9a4f7ab57125fd7cf5671124f5c0a14e21f9beb50cb13/pytoml11-0.0.5.tar.gz --output /work/pytoml11.tar.gz \
    && echo '22ee71a9094052cd3b049e787709ba807646fdd02a1447782cdd23d40b0c5af9  /work/pytoml11.tar.gz' | sha256sum --check \
    && mkdir /work/pytoml11-source \
    && tar -xzf /work/pytoml11.tar.gz --strip-components=1 -C /work/pytoml11-source \
    && cd /work/pytoml11-source \
    && printf '%s\n' \
       '013d4da0a07d15a3f4ce135963680899500db3f6ab2a15c82f94ca4508dd40b1  src/pytoml11.cpp' \
       '2dd8d6065152fa4ced2756a79ae23cbe054358b676407e8306a40b0d33668c8c  src/toml.hpp' \
       '8eec357e0c780cada904923086752c0f85cf4bac34e957d68ae1d46ef6d2ddba  src/pytoml11/__init__.py' \
       'aeb42ddc3196e47e1cef118a4296f34abd77d9cfd53545412924c66c38330a67  CMakeLists.txt' \
       'b7a5800b20d8723bf0063ff16ad32180905494e5a11e712778775094c9fffa8e  pyproject.toml' \
       '6b3e46b19c48ed94f2fa911503b91e9be759b36e6c5a709082ab3e954b441ca0  LICENCE' \
       | sha256sum --check \
    && grep -Fx 'Version: 0.0.5' PKG-INFO \
    && grep -F 'License :: OSI Approved :: MIT License' pyproject.toml \
    && grep -Fx '#define TOML11_VERSION_MINOR 2' src/toml.hpp
COPY build-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# clang 16: the vendored toml11 needs std::source_location, which clang 14 cannot compile with libstdc++ 12.
# Every translation unit carries LLVM coverage mapping; the merge step keeps only the vendored toml11
# header as parser source and counts pytoml11's own pybind11 source as wrapper lines.
RUN cd /work/pytoml11-source \
    && CC=clang-16 CXX=clang++-16 \
       CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       CXXFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' \
       /opt/venv/bin/pip install --no-build-isolation --no-deps --no-index . \
    && diff -r --exclude=__pycache__ --exclude='_value*.so' /work/pytoml11-source/src/pytoml11 /opt/venv/lib/python3.11/site-packages/pytoml11 \
    && cd /tmp \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import pytoml11; from importlib.metadata import version; assert version("pytoml11") == "0.0.5"; print(pytoml11.loads("ready = true\n").value)'
RUN { python3 --version; clang-16 --version | head -1; llvm-cov-16 --version | grep -i version | head -1; cmake --version | head -1; \
      /opt/venv/bin/pip show pytoml11 pybind11 scikit-build-core | grep -E '^(Name|Version):'; \
      echo 'toml11 4.2.0 single header vendored at src/toml.hpp'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-pytoml11-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
# clang 16 profiles need the matching llvm-profdata and llvm-cov; the Parsarium LLVM bridge calls them from PATH.
ENV PATH=/usr/lib/llvm-16/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm-16 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/pytoml11-source /work/pytoml11-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY expected /work/expected
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
