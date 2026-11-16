FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/27/d1/275bf448af16320ebc6261fe4fac24ca4760944a46d1680d796f7c54d10b/imgio-1.7.4-py3-none-any.whl --output /work/wheels/imgio-1.7.4-py3-none-any.whl \
    && echo 'dcb18caea26fb6e5902492caa1c60e9ae47537aeedf4d0d6877d992670568210  /work/wheels/imgio-1.7.4-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7d/8a/3b7f62b9df56460959f1b9bef094248d2a4d7f393c5b0d2da8efcdf0e40e/imageio-2.38.1-py3-none-any.whl --output /work/wheels/imageio-2.38.1-py3-none-any.whl \
    && echo '36d23eb7423d2fb63f637098758edb3d2df3687f7125e0a5ce8596572022dcf9  /work/wheels/imageio-2.38.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/98/e7/af4573bf5b56b7fc0aa9af2ac42654a68201adff45a439801baa00c22c00/openexr-3.5.3-cp314-cp314-manylinux_2_28_x86_64.whl --output /work/wheels/openexr-3.5.3-cp314-cp314-manylinux_2_28_x86_64.whl \
    && echo 'dd27c20ccfdcd1d8eade0c35f1c5d4502e2a81fcf78c52130aa55619abd11aa5  /work/wheels/openexr-3.5.3-cp314-cp314-manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/1d/f2/1371707ce438ba9a43f9d24089828494ec6f9396e28cd7903aa704dd6306/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'e91c2b1cbeae768c98752e67e717e283d68dae45717b41f2d91eaee648e37b7d  /work/wheels/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/2b/d1/50e0e1a4c153b40cfb8f814abf9e47ae63c2ed280b308d977d23c4496edb/pyexr-0.5.0-py3-none-any.whl --output /work/wheels/pyexr-0.5.0-py3-none-any.whl \
    && echo 'd7c509f038950dce223be063a8ebf28e891eafd0ac9e7fb1b470c4e02898f0de  /work/wheels/pyexr-0.5.0-py3-none-any.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show imgio atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
