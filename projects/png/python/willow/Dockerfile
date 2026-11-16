FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/76/ef/a2e237f856b374e466fba458a6188a73fd68db7fb6b76706ce454980092f/willow-1.12.0-py3-none-any.whl --output /work/wheels/willow-1.12.0-py3-none-any.whl \
    && echo 'd3541690b6726a4f6f4654f80507d81bacfa0c686ab065eb5c90159f1b9cee38  /work/wheels/willow-1.12.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/07/6c/aa3f2f849e01cb6a001cd8554a88d4c77c5c1a31c95bdf1cf9301e6d9ef4/defusedxml-0.7.1-py2.py3-none-any.whl --output /work/wheels/defusedxml-0.7.1-py2.py3-none-any.whl \
    && echo 'a352e7e428770286cc899e2542b6cdaedb2b4953ff269a210103ec58f6198a61  /work/wheels/defusedxml-0.7.1-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/18/79/1b8fa1bb3568781e84c9200f951c735f3f157429f44be0495da55894d620/filetype-1.2.0-py2.py3-none-any.whl --output /work/wheels/filetype-1.2.0-py2.py3-none-any.whl \
    && echo '7ce71b6880181241cf7ac8697a2f1eb6a8bd9b429f7ad6d27b8db9ba5f1c2d25  /work/wheels/filetype-1.2.0-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/1d/f2/1371707ce438ba9a43f9d24089828494ec6f9396e28cd7903aa704dd6306/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'e91c2b1cbeae768c98752e67e717e283d68dae45717b41f2d91eaee648e37b7d  /work/wheels/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show Willow atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
