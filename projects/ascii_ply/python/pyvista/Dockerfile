FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/5e/72/0d1da868fc241bb2ab930ff9b802bbc17a1df7e9f36565769a978d052dbf/pyvista-0.49.2-py3-none-any.whl --output /work/wheels/pyvista-0.49.2-py3-none-any.whl \
    && echo '63f78495b30e146c9d1debeca7fa44c7a3935cc9f9ded8638b809ef955fc167a  /work/wheels/pyvista-0.49.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/64/b4/17d4b0b2a2dc85a6df63d1157e028ed19f90d4cd97c36717afef2bc2f395/attrs-26.1.0-py3-none-any.whl --output /work/wheels/attrs-26.1.0-py3-none-any.whl \
    && echo 'c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309  /work/wheels/attrs-26.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/32/d1/a3652fe2c19134d0d15922177821d863cbd7e842d53a21bbe7e8e3a1b5ac/certifi-2026.10.23-py3-none-any.whl --output /work/wheels/certifi-2026.10.23-py3-none-any.whl \
    && echo 'e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1  /work/wheels/certifi-2026.10.23-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/fc/ad/d07d7862a62ffa6d79d68074d14823243dd235a77c45262acbf6adeb28bf/charset_normalizer-3.5.2-py3-none-any.whl --output /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl \
    && echo 'b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685  /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/cf/8c/9677dad226e5aaac5b823d5b09d881ebc32ff1648af417597649841e516c/contourpy-1.4.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/contourpy-1.4.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'e439ab450c93455feb0218532ded3e946ec7a9b5f459069f122cfa44b89229f6  /work/wheels/contourpy-1.4.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e7/05/c19819d5e3d95294a6f5947fb9b9629efb316b96de511b418c53d245aae6/cycler-0.12.1-py3-none-any.whl --output /work/wheels/cycler-0.12.1-py3-none-any.whl \
    && echo '85cef7cff222d8644161529808465972e51340599459b8ac3ccbac5a854e0d30  /work/wheels/cycler-0.12.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/3b/a2/f06e43bc6e032affbdd54bcd78132713a06e1d5774b29a04c0df94e57fd5/cyclopts-5.4.1-py3-none-any.whl --output /work/wheels/cyclopts-5.4.1-py3-none-any.whl \
    && echo '48a80e4e49a10f7aa0bb99211f6eeb7e4f35b0c79a797c526670522daa35d7f2  /work/wheels/cyclopts-5.4.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a7/5f/ed01f9a3cdffbd5a008556fc7b2a08ddb1cc6ace7effa7340604b1d16699/docstring_parser-0.18.0-py3-none-any.whl --output /work/wheels/docstring_parser-0.18.0-py3-none-any.whl \
    && echo 'b3fcbed555c47d8479be0796ef7e19c2670d428d72e96da63f3a40122860374b  /work/wheels/docstring_parser-0.18.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/35/74/4ea331ecc65ba05a58b1e4e8ccd604c8a15565f876dfbf93fc2a2ea2e22b/fonttools-4.68.0-py3-none-any.whl --output /work/wheels/fonttools-4.68.0-py3-none-any.whl \
    && echo 'd76f8fdcb6936f5e1045a0c9dd721a4bf11112e60d1e243bfa1d39f06a8b3104  /work/wheels/fonttools-4.68.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/58/a2/bb081bab032533a855d44de1d56f8e8426114ff1ba5d1f07a438a0a654f8/idna-3.20-py3-none-any.whl --output /work/wheels/idna-3.20-py3-none-any.whl \
    && echo 'ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c  /work/wheels/idna-3.20-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a1/13/08188f0cafa3a800403e4ff62b9aad4e7a17f9c4c7e080dc8f18c64794cf/kiwisolver-1.5.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/kiwisolver-1.5.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '18a0cfb124546a4c2e6087c5f3029c7f44b37c85b142e0ced71f73a7599ac208  /work/wheels/kiwisolver-1.5.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c9/31/5f0ac2f1a1c67423c995c731a11cd4ad05d081a2be969d74f868bdb9cc70/markdown_it_py-4.3.0-py3-none-any.whl --output /work/wheels/markdown_it_py-4.3.0-py3-none-any.whl \
    && echo '7aa1511a46c39138de78d9eba92ce47e63124d8003fc98b3a351909e04239efa  /work/wheels/markdown_it_py-4.3.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/29/5e/52f56f93d5b20815ee0ae352f7a38eff25580edb180b4fa7df87cfeba68f/matplotlib-3.11.2-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/matplotlib-3.11.2-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo '8c8255de28f986d935a64c9ca71c0ec2d2f41d355691f5ea684725dc91413f71  /work/wheels/matplotlib-3.11.2-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b3/38/89ba8ad64ae25be8de66a6d463314cf1eb366222074cfda9ee839c56a4b4/mdurl-0.1.2-py3-none-any.whl --output /work/wheels/mdurl-0.1.2-py3-none-any.whl \
    && echo '84008a41e51615a49fc9966191ff91509e3c40b939176e643fd50a5c2196b8f8  /work/wheels/mdurl-0.1.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/63/34/ba1c580383c9eada3711951fef0795c80b829a078d72188184bcab9dd527/packaging-26.3-py3-none-any.whl --output /work/wheels/packaging-26.3-py3-none-any.whl \
    && echo 'd7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c  /work/wheels/packaging-26.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/1d/f2/1371707ce438ba9a43f9d24089828494ec6f9396e28cd7903aa704dd6306/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'e91c2b1cbeae768c98752e67e717e283d68dae45717b41f2d91eaee648e37b7d  /work/wheels/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7c/ae/ecbbbfd0e4343a6a521d49b3c8656fb4643dee2a4f6eaf941cf3280391a8/platformdirs-4.14.5-py3-none-any.whl --output /work/wheels/platformdirs-4.14.5-py3-none-any.whl \
    && echo '8e778c6fa421516f4d3369449f8df3b0e1b72c0e0005fe88e3ec772d0a14e750  /work/wheels/platformdirs-4.14.5-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/2a/2d/d4bf65e47cea8ff2c794a600c4fd1273a7902f268757c531e0ee9f18aa58/pooch-1.9.0-py3-none-any.whl --output /work/wheels/pooch-1.9.0-py3-none-any.whl \
    && echo 'f265597baa9f760d25ceb29d0beb8186c243d6607b0f60b83ecf14078dbc703b  /work/wheels/pooch-1.9.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/71/46/17f022dd3e953bf20a04a028a21ec746d942f8d2af30fa0f124fa0e6a684/pygments-2.21.0-py3-none-any.whl --output /work/wheels/pygments-2.21.0-py3-none-any.whl \
    && echo '2363c69b61c4a97c838da3b130dcd6468f4848992b21a82f2a63ec34377137d9  /work/wheels/pygments-2.21.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/38/bb/d215ee7c73b61497b28a5503f9f53523f294fcc936762b7caf90e0c1c2b5/pyparsing-3.3.3-py3-none-any.whl --output /work/wheels/pyparsing-3.3.3-py3-none-any.whl \
    && echo 'ece8c00a69cf01b45d0b1dedabb469c90d8caf996d4fda40f147627a122849a4  /work/wheels/pyparsing-3.3.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/2f/a9/52b89563d154433d79b51ed1eb4842bf7334cb2696891a7fe135618853d7/python_dateutil-4.0.0-py3-none-any.whl --output /work/wheels/python_dateutil-4.0.0-py3-none-any.whl \
    && echo 'a5e246f79eb80475e691bf93862cead98decd8a498cf53ba0516fcdc0f50dc1c  /work/wheels/python_dateutil-4.0.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/75/e7/24d49960620aa770fc1fb527a019ec5a860e27c73bcd69c4bdfcc510c7a7/pyvista_validation-0.2.2-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/pyvista_validation-0.2.2-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'a45b633b89d843329db1608ba2bbed75d075ab63c5a7427c8dfa9ad9c23eadb4  /work/wheels/pyvista_validation-0.2.2-cp310-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a0/f4/c67b0b3f1b9245e8d266f0f112c500d50e5b4e83cb6f3b71b6528104182a/requests-2.34.2-py3-none-any.whl --output /work/wheels/requests-2.34.2-py3-none-any.whl \
    && echo '2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0  /work/wheels/requests-2.34.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/82/3b/64d4899d73f91ba49a8c18a8ff3f0ea8f1c1d75481760df8c68ef5235bf5/rich-15.0.0-py3-none-any.whl --output /work/wheels/rich-15.0.0-py3-none-any.whl \
    && echo '33bd4ef74232fb73fe9279a257718407f169c09b78a87ad3d296f548e27de0bb  /work/wheels/rich-15.0.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/d1/4e/716b42bf066e180c1235783b46f095a5d871d05dca7006d2295aac29c491/rich_rst-2.2.0-py3-none-any.whl --output /work/wheels/rich_rst-2.2.0-py3-none-any.whl \
    && echo '1ea1c43813dc4a8d86475fce27ffb74e0ada3d4656c9f8130ba2a59868055fe9  /work/wheels/rich_rst-2.2.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c2/03/0fe8dc08e063a85e5ec492baa827d1bc1fbea45cdbe54fe1899296d9da96/scooby-0.12.1-py3-none-any.whl --output /work/wheels/scooby-0.12.1-py3-none-any.whl \
    && echo '4e3e474a3542fd1d19d775cea70d19ce58a005102c0206955dddbbd33f07eb4e  /work/wheels/scooby-0.12.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl --output /work/wheels/typing_extensions-4.16.0-py3-none-any.whl \
    && echo '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  /work/wheels/typing_extensions-4.16.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/0a/66/9a06c2227fedfd4919f0eaaa8b94377d9730882a7e4f95823c9a331ab5e1/tzdata-2026.6-py2.py3-none-any.whl --output /work/wheels/tzdata-2026.6-py2.py3-none-any.whl \
    && echo '0a10eec6e13ef16b627fabed9a5f2ba61a62b1c67f327305f4e7e412a70b4aec  /work/wheels/tzdata-2026.6-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/92/9d/c4e665119135114480843e7ab388fa94d8480650450e6f8e26b70d323a4c/urllib3-2.8.0-py3-none-any.whl --output /work/wheels/urllib3-2.8.0-py3-none-any.whl \
    && echo '0cf3cae568d36aa9576b28dfb35f11328f1cb974ca7647d9475ebb86c75ac6e3  /work/wheels/urllib3-2.8.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/20/82/55116286ebd08145e91e1e95ffc879b9a3d01ff2d440975797a98f77b0e3/vtk-9.7.2-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/vtk-9.7.2-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '8a762b8d6a711f1e8c9c58f319efc3aa3d7d4f97902e0045f1a4ccf2849e9345  /work/wheels/vtk-9.7.2-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show pyvista atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
