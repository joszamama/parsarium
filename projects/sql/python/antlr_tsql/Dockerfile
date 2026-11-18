FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY build-requirements.lock /work/
# antlr-tsql 0.12.6 (2019) and its pinned runtime requirements, all sdists: antlr4-python3-runtime
# 4.7.2 (requirements.txt ~=4.7.2), antlr-ast 0.7.0 (~=0.7.0) and PyYAML 5.4.1 (~=5.1; imported by
# antlr_tsql.ast). PyYAML 5.4.1 predates Cython 3, so it is built with Cython 0.29.37 and no
# build isolation; without libyaml headers it installs its pure-Python implementation.
RUN mkdir /work/sdists \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/6d/ef/9c5be4cbe024ebacd45b4c6c7e6418b847ba5b081bfb627b833853a83eb4/antlr-tsql-0.12.6.tar.gz --output /work/sdists/antlr-tsql-0.12.6.tar.gz \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/29/14/8ac135ec7cc9db3f768e2d032776718c6b23f74e63543f0974b4873500b2/antlr4-python3-runtime-4.7.2.tar.gz --output /work/sdists/antlr4-python3-runtime-4.7.2.tar.gz \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e7/a1/49e675cd622984d927921a3fe143fea2f9859c61f6855476b288b7df7c71/antlr-ast-0.7.0.tar.gz --output /work/sdists/antlr-ast-0.7.0.tar.gz \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a0/a4/d63f2d7597e1a4b55aa3b4d6c5b029991d3b824b5bd331af8d4ab1ed687d/PyYAML-5.4.1.tar.gz --output /work/sdists/PyYAML-5.4.1.tar.gz \
    && cd /work/sdists \
    && printf '%s\n' \
       '8b3a41da30b7b8299e316abb08e815e6bfd89e06fa86121ce2da00318605c5f9  antlr-tsql-0.12.6.tar.gz' \
       '168cdcec8fb9152e84a87ca6fd261b3d54c8f6358f42ab3b813b14a7193bb50b  antlr4-python3-runtime-4.7.2.tar.gz' \
       'e675245733f4aa86bdcd0556fa73e3027ca6aa17a66fedf75a87182f4950a90e  antlr-ast-0.7.0.tar.gz' \
       '607774cbba28732bfa802b54baa7484215f530991055bb562efbed5b2f20a45e  PyYAML-5.4.1.tar.gz' \
       | sha256sum --check \
    && mkdir /work/antlr-tsql-sdist \
    && tar -xzf antlr-tsql-0.12.6.tar.gz --strip-components=1 -C /work/antlr-tsql-sdist \
    && cd /work/antlr-tsql-sdist \
    && printf '%s\n' \
       '01efe24cff41acbc8d7551b7c97b85e8c8de83a42e8aee4fac4dd2281c0e3f16  antlr_tsql/ast.py' \
       '05833d9a22ed93aeaef43e855564cc6c92d9d9311fa717bf17366e725966ffa5  antlr_tsql/antlr_py/tsqlParser.py' \
       '8486a10c4393cee1c25392769ddd3b2d6c242d6ec7928e1414efff7dfb2f07ef  LICENSE' \
       | sha256sum --check \
    && grep -q 'GNU AFFERO GENERAL PUBLIC LICENSE' LICENSE
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock \
    && for sdist in PyYAML-5.4.1 antlr4-python3-runtime-4.7.2 antlr-ast-0.7.0 antlr-tsql-0.12.6; do \
         /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps "/work/sdists/$sdist.tar.gz" || exit 1; \
       done \
    && /opt/venv/bin/pip uninstall -y cython wheel \
    && /opt/venv/bin/pip check \
    && diff -r --exclude=__pycache__ /work/antlr-tsql-sdist/antlr_tsql /opt/venv/lib/python3.11/site-packages/antlr_tsql \
    && cd /tmp && /opt/venv/bin/python -c 'import antlr_tsql; from antlr_tsql import ast; assert antlr_tsql.__version__ == "0.12.6"; print(type(ast.parse("SELECT a FROM b")).__name__)' \
    && { python3 --version; /opt/venv/bin/pip show antlr-tsql antlr-ast antlr4-python3-runtime PyYAML setuptools | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
