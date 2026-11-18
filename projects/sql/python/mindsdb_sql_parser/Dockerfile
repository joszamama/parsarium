FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY build-requirements.lock /work/
# mindsdb_sql_parser 0.13.8: pure-Python sdist only (no wheel on PyPI). It installs the
# mindsdb_sql_parser package and the SLY 0.5 lexer/LALR library it vendors as the top-level sly package.
# The installed packages must match the sdist byte for byte (the build step's parser-table
# regeneration must not change parser.json).
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f8/b6/4e28de83d1cc4b62d540fee2d5cdd71f46a69698c254fe107532e4b7ab09/mindsdb_sql_parser-0.13.8.tar.gz --output /work/mindsdb.tar.gz \
    && echo '2c077a92883c11a6ccfe0f7095e5e575d2c58a4fdaa53fa7867a0d9c4ad563e3  /work/mindsdb.tar.gz' | sha256sum --check \
    && mkdir /work/mindsdb-sdist \
    && tar -xzf /work/mindsdb.tar.gz --strip-components=1 -C /work/mindsdb-sdist \
    && cd /work/mindsdb-sdist \
    && printf '%s\n' \
       '2504eed4370d9e986442bc467b55f755c8d782916ccd9c83561b1f7cc5553f50  mindsdb_sql_parser/parser.py' \
       '02e645797cd13e264d7f629b5d571e475db9d0c185ad5e84f37ffa6001363344  mindsdb_sql_parser/lexer.py' \
       'ad310c68bffb05a20a917c0e916381d7c8f5d88d1b6ef56c80bb5b713e433414  sly/yacc.py' \
       '9fab7ef7e832d1d154dc7fe4821516c0e7f91634c0b819f4298cb6a39fde1e08  LICENSE' \
       | sha256sum --check \
    && grep -qx 'MIT License' LICENSE \
    && grep -qx "__version__ = '0.13.8'" mindsdb_sql_parser/__about__.py
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock \
    && /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/mindsdb-sdist -w /work/wheels \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/mindsdb_sql_parser-0.13.8-*.whl \
    && diff -r --exclude=__pycache__ /work/mindsdb-sdist/mindsdb_sql_parser /opt/venv/lib/python3.11/site-packages/mindsdb_sql_parser \
    && diff -r --exclude=__pycache__ /work/mindsdb-sdist/sly /opt/venv/lib/python3.11/site-packages/sly \
    && cd /tmp && /opt/venv/bin/python -c 'from mindsdb_sql_parser import parse_sql; print(type(parse_sql("SELECT 1")).__name__)' \
    && { python3 --version; /opt/venv/bin/pip show mindsdb_sql_parser setuptools | grep -E '^(Name|Version):'; } > /work/toolchain.txt

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
