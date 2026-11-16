FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv python3-setuptools python3-wheel \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e5/ed/caf087d2d65ceef10fb117af79bbab50ea3a24ed8b1dc8abb0dc8039d2d3/pdfquery-0.4.3.tar.gz --output /work/wheels/pdfquery-0.4.3.tar.gz \
    && echo 'a2a2974cb312fda4f569adc8d63377d25d5c6367240b4a7bfb165392c73e1dce  /work/wheels/pdfquery-0.4.3.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e9/02/4e7d553a7ac4b4238b38b3c1b80d486e9d4436f8d2acbf87a0997fe3f402/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo 'b0431303acaea1089ad4b3e9ce4e6518193def1118d4073ca848635ee4ea2e96  /work/wheels/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/cc/75/88a3eb36264375ff951bd2f9397c409727ab6aa6a18e1bd933851571d421/chardet-7.7.0-py3-none-any.whl --output /work/wheels/chardet-7.7.0-py3-none-any.whl \
    && echo '11cf9b719ea3675a2a7d8a3071bbe4d7ea24b26bfe39a51588d515ddd05cacad  /work/wheels/chardet-7.7.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/fc/ad/d07d7862a62ffa6d79d68074d14823243dd235a77c45262acbf6adeb28bf/charset_normalizer-3.5.2-py3-none-any.whl --output /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl \
    && echo 'b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685  /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/21/69/64cef1f702bf6657e0cc186ed1a2891d50d29fb41586b254e1c07adea261/cryptography-50.0.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/cryptography-50.0.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '630ebfea3bf689d075f82316324ff7433dc447fe6bc1bfc76524b74b4a9567d2  /work/wheels/cryptography-50.0.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/08/ae/f24b3aac56ba91a29c9d3a31c07a9ad4e9eb500e5d212742bb6d348edaef/cssselect-1.6.0-py3-none-any.whl --output /work/wheels/cssselect-1.6.0-py3-none-any.whl \
    && echo '6df6eab9b264c0f2092a6e386b33610e1684a25e27925ecebe25e3d97cbf3525  /work/wheels/cssselect-1.6.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/66/bc/6230cf80e4331c33383b0b6b73dc31a393dd76edd4cb73d761de5123034d/lxml-6.1.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/lxml-6.1.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo 'c6c0c13128a32eb04a51357e56a094e13aa8e6d3d1884de2e9ae923f6915e1a8  /work/wheels/lxml-6.1.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/20/8b/28c4eaec9d6b036a52cb44720408f26b1a143ca9bce76cc19e8f5de00ab4/pdfminer_six-20260107-py3-none-any.whl --output /work/wheels/pdfminer_six-20260107-py3-none-any.whl \
    && echo '366585ba97e80dffa8f00cebe303d2f381884d8637af4ce422f1df3ef38111a9  /work/wheels/pdfminer_six-20260107-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b6/ae/315bbeee126a769cbde43cf4908acb4b40408d8bf8bbf334dd7368d8dadf/pycparser-3.12-py3-none-any.whl --output /work/wheels/pycparser-3.12-py3-none-any.whl \
    && echo 'a076f3f489b39b43ed13563a1dafe42447445bec2e294154ec5c57fcdda4c85e  /work/wheels/pycparser-3.12-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/2f/d2/5eab7f15bdb63c5281f625a003e999ef3f843c35972c936b07ea868cb854/pyquery-2.1.0-py3-none-any.whl --output /work/wheels/pyquery-2.1.0-py3-none-any.whl \
    && echo '74c9e65ea0cfbcf644a8c3fd438a3dedbcbbd497b9cb366a4f360dba72f8aebb  /work/wheels/pyquery-2.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b7/ce/149a00dd41f10bc29e5921b496af8b574d8413afcd5e30dfa0ed46c2cc5e/six-1.17.0-py2.py3-none-any.whl --output /work/wheels/six-1.17.0-py2.py3-none-any.whl \
    && echo '4721f391ed90541fddacab5acf947aa0d3dc7d27b2e1e8eda2be8970586c3274  /work/wheels/six-1.17.0-py2.py3-none-any.whl' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl \
    && /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps /work/wheels/pdfquery-0.4.3.tar.gz
RUN { python3 --version; /opt/venv/bin/pip show pdfquery atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
