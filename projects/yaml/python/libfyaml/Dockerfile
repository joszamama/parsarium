FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm ninja-build pkg-config python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# libfyaml 1.0.0rc2 on PyPI is the python-libfyaml directory of the libfyaml v1.0.0-rc2 tag; its
# setup.py builds the bundled C library from the repository root (src/, include/), which the sdist
# does not carry. The image pins both, checks that the sdist's Python package and setup.py are
# identical to the tag's python-libfyaml, and builds from the tag tree.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/6c/85/0a9c4b8f9fb12e8154abaa3df65247caef8f13bf412800e58db3594f54e7/libfyaml-1.0.0rc2.tar.gz --output /work/libfyaml-sdist.tar.gz \
    && echo '419e95961d5e0f3b82e65a65551e0c0a8f1c964163e6e44476f384bdd3ca5a0f  /work/libfyaml-sdist.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/pantoniou/libfyaml/tar.gz/refs/tags/v1.0.0-rc2 --output /work/libfyaml-src.tar.gz \
    && echo 'd8406971663c7624d15768ecbc78e56445de14b4cf40898fbe487925fafae7fd  /work/libfyaml-src.tar.gz' | sha256sum --check \
    && mkdir /work/sdist /work/libfyaml-src \
    && tar -xzf /work/libfyaml-sdist.tar.gz --strip-components=1 -C /work/sdist \
    && tar -xzf /work/libfyaml-src.tar.gz --strip-components=1 -C /work/libfyaml-src \
    && diff -r /work/sdist/libfyaml /work/libfyaml-src/python-libfyaml/libfyaml \
    && cmp /work/sdist/setup.py /work/libfyaml-src/python-libfyaml/setup.py \
    && cmp /work/sdist/LICENSE /work/libfyaml-src/python-libfyaml/LICENSE \
    && printf '%s\n' \
       '1c71a7e4032140af2170ca37a305fc740491c32140d3d27f4e07dbbcc64a2049  /work/libfyaml-src/src/lib/fy-parse.c' \
       '3746a7e8dfbecf0415304169d2ef7fc08d58e2892605d8ac266a1741eee31ecf  /work/libfyaml-src/src/lib/fy-input.c' \
       '9fa2994e4422fa5a23b92a111072f527749afc752607bd10c68fce83564a823b  /work/libfyaml-src/python-libfyaml/libfyaml/_libfyaml.c' \
       '8c6ab373d0f40d39fc976227010f22a52e83e0e40fd25e5ac8f19945fed8aa5a  /work/libfyaml-src/LICENSE' \
       '22e1ad17907b05ecceb1c4225e9be5b6e88f8544f8640bc851a59a41b71e0910  /work/libfyaml-src/python-libfyaml/LICENSE' \
       | sha256sum --check \
    && grep -Fx 'Version: 1.0.0rc2' /work/sdist/PKG-INFO
COPY build-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# setup.py builds the bundled static libfyaml with CMake (extra arguments through its documented
# LIBFYAML_CMAKE_ARGS) and links it into libfyaml/_libfyaml.abi3.so; both the library and the
# binding are compiled with clang -O0 and LLVM source coverage.
RUN cd /work/libfyaml-src/python-libfyaml \
    && CC=clang CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
       LIBFYAML_CMAKE_ARGS="-DCMAKE_C_COMPILER=clang -DCMAKE_BUILD_TYPE=Debug '-DCMAKE_C_FLAGS=-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'" \
       /opt/venv/bin/pip install --no-build-isolation --no-deps --no-index . \
    && module=$(find /opt/venv/lib/python3.14/site-packages/libfyaml -maxdepth 1 -name '_libfyaml*.so' -print -quit) \
    && test -n "$module" && ! ldd "$module" | grep -q fyaml \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import libfyaml; from importlib.metadata import version; assert version("libfyaml") == "1.0.0rc2"; print(libfyaml.loads("ready: true").to_python())'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; cmake --version | head -1; \
      /opt/venv/bin/pip show libfyaml setuptools | grep -E '^(Name|Version):'; \
      cd /work/libfyaml-src/src/lib && sha256sum fy-parse.c fy-input.c; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-libfyaml-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/libfyaml-src/src /work/libfyaml-src/src
COPY --from=build /work/libfyaml-src/include /work/libfyaml-src/include
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh expected.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
