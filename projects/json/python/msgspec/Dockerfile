FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl clang libclang-rt-14-dev llvm python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY build-requirements.lock /work/
# msgspec 0.22.0 sdist; its _core.c, atof.h and LICENSE match the 0.22.0 tag (commit 6d3443f2dae8413a1a56640290c09a6f486f30c2).
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/d0/e6/6dcf9306ff3c5e486578f3bf29ed11dfbdbbc2a8bf0caf7e07d392887fda/msgspec-0.22.0.tar.gz -o /work/msgspec.tar.gz \
    && echo '0a13624a4969159fe35d8c2a3d377b2b61bbd8585e327440d5e52725affcce38  /work/msgspec.tar.gz' | sha256sum --check \
    && mkdir -p /work/msgspec-source \
    && tar -xzf /work/msgspec.tar.gz -C /work/msgspec-source --strip-components=1 \
    && cd /work/msgspec-source \
    && printf '%s\n' \
       '83b0fef8973a212310447e3891ec62a704a8e11d4be1fe942f5326f6e2c9179c  src/msgspec/_core.c' \
       '628e0c82a742fd3ae6b6f5abaacb980872aebd7b5ba326515cbfa45b034d7dc0  src/msgspec/atof.h' \
       '6fde8b6723885e8508808f65ac372feb97d3eee2eab2b91d34d796b75b7ac734  LICENSE' \
       | sha256sum --check
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# msgspec's setup.py builds the single msgspec._core extension; MSGSPEC_DEBUG stays unset so asserts stay off as in release builds.
RUN cd /work/msgspec-source \
    && CC=clang LDSHARED='clang -shared' \
       CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' \
       /opt/venv/bin/pip install --no-build-isolation --no-deps . \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import msgspec; assert msgspec.__version__ == "0.22.0", msgspec.__version__; print(msgspec.json.decode(b"{\"ready\":true}"))'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; /opt/venv/bin/pip show msgspec setuptools setuptools-scm | grep -E '^(Name|Version):'; echo 'msgspec tag 0.22.0 commit 6d3443f2dae8413a1a56640290c09a6f486f30c2'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-msgspec-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/msgspec-source /work/msgspec-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
