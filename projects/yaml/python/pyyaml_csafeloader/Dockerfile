FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# PyYAML 6.0.3 sdist (Python package and the _yaml.pyx binding) and libyaml 0.2.5, the
# libyaml release the official PyYAML 6.0.3 wheels link statically.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/05/8e/961c0007c59b8dd7729d542c61a4d537767a59645b82a0b521206e1e25c2/pyyaml-6.0.3.tar.gz --output /work/pyyaml.tar.gz \
    && echo 'd76623373421df22fb4cf8817020cbb7ef15c725b9d5e45f17e189bfc384190f  /work/pyyaml.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://pyyaml.org/download/libyaml/yaml-0.2.5.tar.gz --output /work/libyaml.tar.gz \
    && echo 'c642ae9b75fee120b2d96c712538bd2cf283228d2337df2cf2988e3c02678ef4  /work/libyaml.tar.gz' | sha256sum --check \
    && mkdir /work/pyyaml-src /work/libyaml-src \
    && tar -xzf /work/pyyaml.tar.gz --strip-components=1 -C /work/pyyaml-src \
    && tar -xzf /work/libyaml.tar.gz --strip-components=1 -C /work/libyaml-src \
    && printf '%s\n' \
       '65efc5f00591ca6d5771a64790d6dbae69677a0d723736b7c2994386a5761313  /work/pyyaml-src/yaml/_yaml.pyx' \
       '2cdd5a11a860f986cb96ba06b0ca1704ee2ab016268c808fa4f85a30601be600  /work/pyyaml-src/yaml/_yaml.pxd' \
       '8d3928f9dc4490fd635707cb88eb26bd764102a7282954307d3e5167a577e8a4  /work/pyyaml-src/LICENSE' \
       'bc3b30ceec0c696925e9703845874d7fafefb42bfbd3006dc4a02fc6d646f2d1  /work/libyaml-src/src/scanner.c' \
       'b418ed8d6ef7e86dbd0e59c8dc7a00c8e48200b0252dd41e25d00d4616c7b2dc  /work/libyaml-src/src/parser.c' \
       'c428a44b177391557bdf49177c1dc0216edf2a2bbe0e24ca2ef2725ef7f01e9d  /work/libyaml-src/src/reader.c' \
       '71f9263a2c77237762c8fa5e7c3d2bdd35723ecf1e2898222c7a603a5bf3f2db  /work/libyaml-src/src/api.c' \
       'c40112449f254b9753045925248313e9270efa36d226b22d82d4cc6c43c57f29  /work/libyaml-src/License' \
       | sha256sum --check \
    && grep -Fx 'License: MIT' /work/pyyaml-src/PKG-INFO
COPY build-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# libyaml as a static PIC archive with LLVM source coverage, linked into PyYAML's _yaml extension.
RUN mkdir -p /opt/libyaml/lib /opt/libyaml/include /work/libyaml-obj \
    && for name in api reader scanner parser loader writer emitter dumper; do \
         clang -std=gnu11 -O0 -g -fPIC -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping \
           -DYAML_VERSION_MAJOR=0 -DYAML_VERSION_MINOR=2 -DYAML_VERSION_PATCH=5 '-DYAML_VERSION_STRING="0.2.5"' \
           -I/work/libyaml-src/include -c /work/libyaml-src/src/$name.c -o /work/libyaml-obj/$name.o || exit 1; \
       done \
    && ar rcs /opt/libyaml/lib/libyaml.a /work/libyaml-obj/*.o \
    && cp /work/libyaml-src/include/yaml.h /opt/libyaml/include/
# Only libyaml carries coverage mapping; the Cython-generated binding is compiled plainly and the
# profile runtime is linked in for the libyaml objects.
RUN cd /work/pyyaml-src \
    && PYYAML_FORCE_CYTHON=1 PYYAML_FORCE_LIBYAML=1 CC=clang LDSHARED='clang -shared' \
       CFLAGS='-O0 -g -fno-omit-frame-pointer -I/opt/libyaml/include' \
       LDFLAGS='-fprofile-instr-generate -L/opt/libyaml/lib' \
       /opt/venv/bin/pip install --no-build-isolation --no-deps --no-index . \
    && diff -r --exclude=__pycache__ --exclude='_yaml.cpython-*.so' /work/pyyaml-src/lib/yaml /opt/venv/lib/python3.14/site-packages/yaml \
    && ! ldd /opt/venv/lib/python3.14/site-packages/yaml/_yaml.cpython-314-aarch64-linux-gnu.so | grep -q libyaml \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import yaml; from yaml import _yaml; assert yaml.__version__ == "6.0.3" and yaml.__with_libyaml__; assert _yaml.get_version_string() == "0.2.5"; assert issubclass(yaml.CSafeLoader, _yaml.CParser); print(yaml.load(b"ready: true", Loader=yaml.CSafeLoader))'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; \
      /opt/venv/bin/pip show PyYAML Cython setuptools | grep -E '^(Name|Version):'; echo 'libyaml 0.2.5 (static, source-built)'; \
      cd /work/libyaml-src/src && sha256sum scanner.c parser.c reader.c api.c; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-pyyaml-c-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/libyaml-src /work/libyaml-src
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh expected.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
