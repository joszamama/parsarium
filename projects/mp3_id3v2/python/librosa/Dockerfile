FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
ENV NUMBA_CACHE_DIR=/tmp/numba-cache NUMBA_DISABLE_JIT=1
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/96/14/0b2e4cc8017796dc8f69de740708601832c1e8d5377166eedb4db0a92264/librosa-1.0.0-py3-none-any.whl --output /work/wheels/librosa-1.0.0-py3-none-any.whl \
    && echo '5910a6c0e1b2e494b92758c1615a7acbd0515a2315e138927ba2982f2af88857  /work/wheels/librosa-1.0.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/32/d1/a3652fe2c19134d0d15922177821d863cbd7e842d53a21bbe7e8e3a1b5ac/certifi-2026.10.23-py3-none-any.whl --output /work/wheels/certifi-2026.10.23-py3-none-any.whl \
    && echo 'e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1  /work/wheels/certifi-2026.10.23-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e9/02/4e7d553a7ac4b4238b38b3c1b80d486e9d4436f8d2acbf87a0997fe3f402/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo 'b0431303acaea1089ad4b3e9ce4e6518193def1118d4073ca848635ee4ea2e96  /work/wheels/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/fc/ad/d07d7862a62ffa6d79d68074d14823243dd235a77c45262acbf6adeb28bf/charset_normalizer-3.5.2-py3-none-any.whl --output /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl \
    && echo 'b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685  /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/88/39/799be3f2f0f38cc727ee3b4f1445fe6d5e4133064ec2e4115069418a5bb6/cloudpickle-3.1.2-py3-none-any.whl --output /work/wheels/cloudpickle-3.1.2-py3-none-any.whl \
    && echo '9acb47f6afd73f60dc1df93bb801b472f05ff42fa6c84167d25cb206be1fbf4a  /work/wheels/cloudpickle-3.1.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/05/7f/798705f5296a58ca505d600456748d1be48078eac8a7050d8a98bc9edb89/decorator-5.3.1-py3-none-any.whl --output /work/wheels/decorator-5.3.1-py3-none-any.whl \
    && echo 'f47fe6fdbd2edd623ecfe36875d37aba411624e2670dd395dddae1358689bb3c  /work/wheels/decorator-5.3.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/58/a2/bb081bab032533a855d44de1d56f8e8426114ff1ba5d1f07a438a0a654f8/idna-3.20-py3-none-any.whl --output /work/wheels/idna-3.20-py3-none-any.whl \
    && echo 'ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c  /work/wheels/idna-3.20-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/18/53/84099323c2ec4be98d935f63c033ac4151ee83836ca1050ede3b3aadf155/joblib-1.6.0-py3-none-any.whl --output /work/wheels/joblib-1.6.0-py3-none-any.whl \
    && echo '3dbbf9f6e4b592a2357b854608e980fe6390d131d7a82f011a377ef2ebef7aba  /work/wheels/joblib-1.6.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/23/93/4e45e37f26c820216704b36b8e67cc55c490a7abd287a78a26a2c0e21386/lazy_loader-0.6-py3-none-any.whl --output /work/wheels/lazy_loader-0.6-py3-none-any.whl \
    && echo '77253be3391b06124a0e16105bd663b6c54470af1a9ca8e1cf026f38d58ed056  /work/wheels/lazy_loader-0.6-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/5c/ed/54107648386edf3da7def03d42721c72279f6bc2e17b5274c18955dc5833/llvmlite-0.50.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/llvmlite-0.50.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo '33ddf12b1e12d7e551e1c1e6ca8087d0aacc931f480019eb33ef2ab77681da4d  /work/wheels/llvmlite-0.50.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/39/8f/bf975b5d2111e4954a0f8567fc6b60bab22c8766dd4fa509af1334c91a4f/msgpack-1.2.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/msgpack-1.2.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl \
    && echo '5d65b791ce4283e02b6267742ad540899155e1b32887b9cbdda47f38f5a076b5  /work/wheels/msgpack-1.2.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/cf/82/8ef9c7e0f50493307a49c09cfa7f00c5a778b6d1921f7b2dabe1d3a5809e/narwhals-2.28.0-py3-none-any.whl --output /work/wheels/narwhals-2.28.0-py3-none-any.whl \
    && echo '1f69d6385ec30e2fa6e1fdeb37c562ecabd0f713f6f3e3b58a668c5c9df9567f  /work/wheels/narwhals-2.28.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/59/1a/0e9a4cf86e470db73a27af634bc43219a475e258e8a66f2da173816543b5/numba-0.68.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numba-0.68.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'b4d210701b32d1d4ffe26d5fc4e96c6b47e2c5d6c4c1a0f76dc48c156ef295ea  /work/wheels/numba-0.68.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/63/34/ba1c580383c9eada3711951fef0795c80b829a078d72188184bcab9dd527/packaging-26.3-py3-none-any.whl --output /work/wheels/packaging-26.3-py3-none-any.whl \
    && echo 'd7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c  /work/wheels/packaging-26.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7c/ae/ecbbbfd0e4343a6a521d49b3c8656fb4643dee2a4f6eaf941cf3280391a8/platformdirs-4.14.5-py3-none-any.whl --output /work/wheels/platformdirs-4.14.5-py3-none-any.whl \
    && echo '8e778c6fa421516f4d3369449f8df3b0e1b72c0e0005fe88e3ec772d0a14e750  /work/wheels/platformdirs-4.14.5-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/2a/2d/d4bf65e47cea8ff2c794a600c4fd1273a7902f268757c531e0ee9f18aa58/pooch-1.9.0-py3-none-any.whl --output /work/wheels/pooch-1.9.0-py3-none-any.whl \
    && echo 'f265597baa9f760d25ceb29d0beb8186c243d6607b0f60b83ecf14078dbc703b  /work/wheels/pooch-1.9.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b6/ae/315bbeee126a769cbde43cf4908acb4b40408d8bf8bbf334dd7368d8dadf/pycparser-3.12-py3-none-any.whl --output /work/wheels/pycparser-3.12-py3-none-any.whl \
    && echo 'a076f3f489b39b43ed13563a1dafe42447445bec2e294154ec5c57fcdda4c85e  /work/wheels/pycparser-3.12-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a0/f4/c67b0b3f1b9245e8d266f0f112c500d50e5b4e83cb6f3b71b6528104182a/requests-2.34.2-py3-none-any.whl --output /work/wheels/requests-2.34.2-py3-none-any.whl \
    && echo '2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0  /work/wheels/requests-2.34.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/86/4e/0bab75490ca4b85fad8388739c7ebc71d9db553f8c69e39943ee8db0aaae/scikit_learn-1.9.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/scikit_learn-1.9.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo '993d332ff80e62efae9e39603b7e872297c418d780f01a01855269a3489c950f  /work/wheels/scikit_learn-1.9.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/6b/89/2a844506d49651e9aa1af6ef95b6bd8031cb1d5a4375edec6155037e04cf/scipy-1.18.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/scipy-1.18.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'ac0333bdf38309aa3dcbe7e3fa7ea29e7a2c37c6ea306a757b700ded8e4596ad  /work/wheels/scipy-1.18.1-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b1/d1/5e338af9ca6ed0786cd5bb03f6d60de1c325728c1189014f3b59aae7403c/soundfile-0.14.0-py2.py3-none-any.whl --output /work/wheels/soundfile-0.14.0-py2.py3-none-any.whl \
    && echo '8ba81ae3a89fd5ab3bef8a8eb481fbbe794e806309675a89b4df48b8d31908a8  /work/wheels/soundfile-0.14.0-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/5c/f1/0e55195893228609c9a08c3b13b7a83a46c3a992cd00d3304f0f320cfb07/soxr-1.1.0-cp312-abi3-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/soxr-1.1.0-cp312-abi3-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo '3b033078e86f3c4a658e5697fac8995764fad9e799563616b630136b613167f1  /work/wheels/soxr-1.1.0-cp312-abi3-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/54/1b/831f2de4840a25db1dd7b1afea433ccafe6bb10aca07e13264f2079462d0/threadpoolctl-3.8.0-py3-none-any.whl --output /work/wheels/threadpoolctl-3.8.0-py3-none-any.whl \
    && echo 'f1b49c82704d50f13ffae019c727b0fa4f6791a58f48f06a09c45face1be66da  /work/wheels/threadpoolctl-3.8.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl --output /work/wheels/typing_extensions-4.16.0-py3-none-any.whl \
    && echo '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  /work/wheels/typing_extensions-4.16.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/92/9d/c4e665119135114480843e7ab388fa94d8480650450e6f8e26b70d323a4c/urllib3-2.8.0-py3-none-any.whl --output /work/wheels/urllib3-2.8.0-py3-none-any.whl \
    && echo '0cf3cae568d36aa9576b28dfb35f11328f1cb974ca7647d9475ebb86c75ac6e3  /work/wheels/urllib3-2.8.0-py3-none-any.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show librosa atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 libsndfile1 && rm -rf /var/lib/apt/lists/*
ENV NUMBA_CACHE_DIR=/tmp/numba-cache NUMBA_DISABLE_JIT=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
