FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# sqlparse 0.6.1: pure-Python py3-none-any wheel; its sqlparse/ package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/sqlparse-sdist /work/sqlparse-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/df/ff/2fee788e82e75be8f210c65c5d103bf44c880e3769c884652a4cd911b8ba/sqlparse-0.6.1-py3-none-any.whl --output /work/wheels/sqlparse-0.6.1-py3-none-any.whl \
    && echo '3be5a72d04c873d690d7c6dedd33d6fae2ef82759881ceec02fc2efd0cba564f  /work/wheels/sqlparse-0.6.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7e/e0/361c764ea58cc1a75f7b4b424a74b08449db8bfa5e9199c7275999fdd1b9/sqlparse-0.6.1.tar.gz --output /work/sqlparse-sdist.tar.gz \
    && echo 'ca722573f848ff2d30e40ea30f53a104b7dea7635ea9285891263eb2c58fb6e7  /work/sqlparse-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/sqlparse-sdist.tar.gz --strip-components=1 -C /work/sqlparse-sdist \
    && unzip -q /work/wheels/sqlparse-0.6.1-py3-none-any.whl -d /work/sqlparse-wheel \
    && diff -r /work/sqlparse-sdist/sqlparse /work/sqlparse-wheel/sqlparse \
    && ! grep '^Requires-Dist:' /work/sqlparse-wheel/sqlparse-0.6.1.dist-info/METADATA | grep -v 'extra ==' \
    && cd /work/sqlparse-sdist \
    && printf '%s\n' \
       'd0912101c641e5da59b0c14c6c24a7ad5abcc7a9e60b22b6574ee98bbf9d83f7  sqlparse/engine/grouping.py' \
       '86c32dd25e3273149f6c6a163c8fd0dbdae399de494b2e2bdfec9f4fbde5817c  sqlparse/lexer.py' \
       'c1938235b80d39e93138eae89edc3af67e18ecbc40d266529fa57b2dce426310  LICENSE' \
       | sha256sum --check \
    && grep -q 'Redistribution and use in source and binary forms' LICENSE
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/sqlparse-wheel/sqlparse /opt/venv/lib/python3.14/site-packages/sqlparse \
    && /opt/venv/bin/python -c 'import sqlparse; assert sqlparse.__version__ == "0.6.1"; print(sqlparse.parse("SELECT 1;")[0].get_type())' \
    && { python3 --version; /opt/venv/bin/pip show sqlparse atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum sqlparse/engine/grouping.py sqlparse/lexer.py; } > /work/toolchain.txt

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
