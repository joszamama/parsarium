FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ff/6b/a2e4390e233f80978700b1b6aaa6523a5d828eaa195460c2dab9e5599b32/omni_archive-0.0.2-py3-none-any.whl --output /work/wheels/omni_archive-0.0.2-py3-none-any.whl \
    && echo '8665417d0f8cf74e7ca45ed25d76f760073de88cdd0efcdf8afb5e25b9a3ce73  /work/wheels/omni_archive-0.0.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/93/d1/a2730d11a79b4b0fa0f2fe9f065882f24a7a09232240fd745f6900cfa1b5/fnmatch2-0.0.8-py2.py3-none-any.whl --output /work/wheels/fnmatch2-0.0.8-py2.py3-none-any.whl \
    && echo '0430ba2b285638d635615317eea3acf5572c457ab885921064d3669923191591  /work/wheels/fnmatch2-0.0.8-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ef/ba/7baa8fe79d48520ae77e594ff1cc1d30a5eb0fefc3846495bcff8bb215a4/pathlib_abc-0.1.1-py3-none-any.whl --output /work/wheels/pathlib_abc-0.1.1-py3-none-any.whl \
    && echo '5cb2f942fdbb75ce0e00ed3b94de9695b0c5d4b419b5004a702da80f165b3109  /work/wheels/pathlib_abc-0.1.1-py3-none-any.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show omni-archive atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
