FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
# git is only queried by rapidyaml's CMake packaging step (c4_proj_get_version); the
# sdist carries no repository, so the version comes from src/ryml/version.py.
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl git libclang-rt-21-dev llvm python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# rapidyaml 0.15.2 sdist: the SWIG interface (cpp/api/ryml.i), the Python package and the
# bundled C++ rapidyaml 0.15.2 and c4core sources it compiles into the _ryml extension.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/8d/5e/80ea1e8ca5785ad52f835f663e8384961bdb258de71a5bd332e99a2d7b20/rapidyaml-0.15.2.tar.gz --output /work/rapidyaml.tar.gz \
    && echo 'a3b075636e6b5673ddf7a50122b029cd44623f18e84bcd4f18425df328425a09  /work/rapidyaml.tar.gz' | sha256sum --check \
    && mkdir /work/ryml-src \
    && tar -xzf /work/rapidyaml.tar.gz --strip-components=1 -C /work/ryml-src \
    && printf '%s\n' \
       'c180f5aed9fb7a948c17160971379f22b862039394d257df12ceccfce6069477  /work/ryml-src/cpp/src/c4/yml/parse_engine.def.hpp' \
       '98368fa54899d9e2daf7718af7c3f0d70e9a1ac997cb4aacf7605c38bc925cc2  /work/ryml-src/cpp/src/c4/yml/tree.cpp' \
       '6669bd8179c056389eff6169ee00c2a3771a0089bf9aa255c6ebe089dfe49934  /work/ryml-src/cpp/src/c4/yml/parse.cpp' \
       'f8c1f0b2786db3031c4ae1f4380c7073b05952338420a0edd6425bfca17eb1ea  /work/ryml-src/cpp/api/ryml.i' \
       'd21acdde3276a3706f41c0a7e911a3953ac1ca6b33c5ae05f92d6651f77ce627  /work/ryml-src/LICENSE.txt' \
       | sha256sum --check \
    && grep -Fx 'License: MIT' /work/ryml-src/PKG-INFO \
    && grep -Fx "__version__ = version = '0.15.2'" /work/ryml-src/src/ryml/version.py
COPY build-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# The package's own setup.py/CMake build (SWIG wrapper plus rapidyaml and c4core compiled into
# ryml/_ryml*.so), with clang -O0 and LLVM source coverage passed through its documented
# CMAKE_FLAGS environment variable.
RUN cd /work/ryml-src \
    && PATH=/opt/venv/bin:$PATH \
       CMAKE_FLAGS="-DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=Debug '-DCMAKE_CXX_FLAGS=-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' '-DCMAKE_C_FLAGS=-O0 -g' -DCMAKE_SHARED_LINKER_FLAGS=-fprofile-instr-generate -DCMAKE_MODULE_LINKER_FLAGS=-fprofile-instr-generate" \
       /opt/venv/bin/pip install --no-build-isolation --no-deps --no-index . \
    && module=$(find /opt/venv/lib/python3.14/site-packages/ryml -maxdepth 1 -name '_ryml*.so' -print -quit) \
    && test -n "$module" \
    && ! ldd "$module" | grep -q ryml \
    && cmp /work/ryml-src/src/ryml/version.py /opt/venv/lib/python3.14/site-packages/ryml/version.py \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import ryml; assert ryml.__version__ == "0.15.2"; t = ryml.parse_in_arena(b"ready: true"); print(bytes(t.key(t.first_child(t.root_id()))))'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; \
      /opt/venv/bin/pip show rapidyaml swig cmake cmake-build-extension setuptools deprecation | grep -E '^(Name|Version):'; \
      cd /work/ryml-src/cpp/src/c4/yml && sha256sum parse_engine.def.hpp parse.cpp tree.cpp; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-ryml-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/ryml-src/cpp /work/ryml-src/cpp
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh expected.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
