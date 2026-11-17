FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# sqlglot 30.33.0: pure-Python py3-none-any wheel; its sqlglot/ package must match the sdist byte for byte.
# The optional sqlglotc (compiled) and sqlglotrs (Rust tokenizer) extras are not installed.
RUN mkdir /work/wheels /work/sqlglot-sdist /work/sqlglot-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/32/b2/564252e22f8e0a383adee6b38afc4a0e38fccbc4046b5c36a387a2308f23/sqlglot-30.33.0-py3-none-any.whl --output /work/wheels/sqlglot-30.33.0-py3-none-any.whl \
    && echo 'a5b279fe7397a9fb6cdd0274a13a5fcee0fa83ac6ff617083f1f2832031e90bc  /work/wheels/sqlglot-30.33.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f6/4d/ce64044d87620a6cfeb0de779359400f29730ad169d7f804c050f8de7c5e/sqlglot-30.33.0.tar.gz --output /work/sqlglot-sdist.tar.gz \
    && echo '9c007e0471c93e778d8613f25853543b959a3f793d9dadf1341b3d6bd53246a8  /work/sqlglot-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/sqlglot-sdist.tar.gz --strip-components=1 -C /work/sqlglot-sdist \
    && unzip -q /work/wheels/sqlglot-30.33.0-py3-none-any.whl -d /work/sqlglot-wheel \
    && diff -r /work/sqlglot-sdist/sqlglot /work/sqlglot-wheel/sqlglot \
    && ! grep '^Requires-Dist:' /work/sqlglot-wheel/sqlglot-30.33.0.dist-info/METADATA | grep -v 'extra ==' \
    && cd /work/sqlglot-sdist \
    && printf '%s\n' \
       '2b871efe5236dcd19bb5727ad5016c31456bded3ba98c50cf169d81a536127e5  sqlglot/parser.py' \
       '93ea4dd996a6ffb9b61f77cc7900658351ca1d9b1d6cd40efddd233720d8e2be  sqlglot/tokens.py' \
       'b0bf909b472ddf9bd4eab30f6e6fd8b33bf3997ce038b882fe0663f291958d2d  LICENSE' \
       | sha256sum --check \
    && grep -qx 'MIT License' LICENSE
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/sqlglot-wheel/sqlglot /opt/venv/lib/python3.14/site-packages/sqlglot \
    && /opt/venv/bin/python -c 'import importlib.util, sqlglot; assert sqlglot.__version__ == "30.33.0"; assert importlib.util.find_spec("sqlglotc") is None and importlib.util.find_spec("sqlglotrs") is None; print(sqlglot.parse_one("SELECT 1").key)' \
    && { python3 --version; /opt/venv/bin/pip show sqlglot atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum sqlglot/parser.py sqlglot/tokens.py; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
