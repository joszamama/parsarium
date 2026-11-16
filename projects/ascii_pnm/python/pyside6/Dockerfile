FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/2f/53/db0cabed1e70d0bc4666b8cbc2611b72bff2f9d2c4813820182621a8c6ee/pyside6-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl --output /work/wheels/pyside6-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl \
    && echo 'd13ed4d0053cc20f3e4e0fdbf12790a9b7f958d7e22c0843411ecfa8c799e2a9  /work/wheels/pyside6-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ff/3e/0d6c5934de575286ac0699a701d4155048185035b8da0ee78d57a38bc7ef/pyside6_addons-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl --output /work/wheels/pyside6_addons-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl \
    && echo '4ab38c0017f0453671a9313d3a53ca1c0e378924f54b07e596bcea94a9642391  /work/wheels/pyside6_addons-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7b/3c/7597d8dcb36aa8315427635ec6ec9d850ffbad4ce78b9118ac854889f2d3/pyside6_essentials-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl --output /work/wheels/pyside6_essentials-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl \
    && echo '16f4b5e41daf49235ae048458243da9efe5f3d8040f9cc5aa454ce69893d3bd9  /work/wheels/pyside6_essentials-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b4/f0/9b4f3cb0506641ea53210c7b635703f1c2c1e81c27074438105ff118f8e7/pyside6_pdf-6.12.0.140-cp310-abi3-manylinux_2_34_x86_64.whl --output /work/wheels/pyside6_pdf-6.12.0.140-cp310-abi3-manylinux_2_34_x86_64.whl \
    && echo '0c94370b6b9d65fbfe54f9d6d25df0677db0cdcfd0a842a63958a3603a42007c  /work/wheels/pyside6_pdf-6.12.0.140-cp310-abi3-manylinux_2_34_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ce/e0/cb8b68b962afc253709ed61555d0a4f297fd6786c0e77921d2e951504210/pyside6_webengine-6.12.0.140-cp310-abi3-manylinux_2_34_x86_64.whl --output /work/wheels/pyside6_webengine-6.12.0.140-cp310-abi3-manylinux_2_34_x86_64.whl \
    && echo 'c041c9921d7c91c9e51a2c027f434d05c3c59baa2c8f17b71dc8194e77791f06  /work/wheels/pyside6_webengine-6.12.0.140-cp310-abi3-manylinux_2_34_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/49/c2/a04fa003b4360e99d8e3fc2829abacf37396ace63ea1cd616402209ec7c6/shiboken6-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl --output /work/wheels/shiboken6-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl \
    && echo '3bde565bb0890044b5c7f63808adddede5abc241e9395a2bfed61919884d6240  /work/wheels/shiboken6-6.12.0-cp310-abi3-manylinux_2_34_x86_64.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show PySide6 atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 libglib2.0-0 libgl1 libegl1 libxkbcommon0 libfreetype6 libglib2.0-0 libfontconfig1 libx11-6 libxcb1 libxrender1 libxext6 libsm6 libice6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
