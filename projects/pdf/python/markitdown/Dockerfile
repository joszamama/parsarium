FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b3/ce/027c1e647909447fa29a5d3eb87d5e98013d49dc0b568602b129a9d06751/markitdown-0.1.9-py3-none-any.whl --output /work/wheels/markitdown-0.1.9-py3-none-any.whl \
    && echo '52f59c48bea9cf887224c56247f648d68beb7aa7af5a12d414748210c83c20ea  /work/wheels/markitdown-0.1.9-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/88/c6/92fcd42f1ba33e1184263f25bfabf3d27c383410470f169e4b8163bf9c17/beautifulsoup4-4.15.0-py3-none-any.whl --output /work/wheels/beautifulsoup4-4.15.0-py3-none-any.whl \
    && echo 'd6f88de62e1d4e38ecb1077eb9724cd0eff29d2a08ca16a401e9b9e93f117cf9  /work/wheels/beautifulsoup4-4.15.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/32/d1/a3652fe2c19134d0d15922177821d863cbd7e842d53a21bbe7e8e3a1b5ac/certifi-2026.10.23-py3-none-any.whl --output /work/wheels/certifi-2026.10.23-py3-none-any.whl \
    && echo 'e9b54de76e530bb6cf0ccd036787103acb58fd42ba930ea8bf948ddbaa2f61d1  /work/wheels/certifi-2026.10.23-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/fc/ad/d07d7862a62ffa6d79d68074d14823243dd235a77c45262acbf6adeb28bf/charset_normalizer-3.5.2-py3-none-any.whl --output /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl \
    && echo 'b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685  /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/31/7d/164b7ffc8624fe9efb4221bf9af485d5c1e41b9ae118045d2b6dc5457d8b/click-8.5.1-py3-none-any.whl --output /work/wheels/click-8.5.1-py3-none-any.whl \
    && echo '8bb5376d2006950386f8c6427613334a2acadc5f559cb80e638d00b4df957e37  /work/wheels/click-8.5.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/07/6c/aa3f2f849e01cb6a001cd8554a88d4c77c5c1a31c95bdf1cf9301e6d9ef4/defusedxml-0.7.1-py2.py3-none-any.whl --output /work/wheels/defusedxml-0.7.1-py2.py3-none-any.whl \
    && echo 'a352e7e428770286cc899e2542b6cdaedb2b4953ff269a210103ec58f6198a61  /work/wheels/defusedxml-0.7.1-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e8/2d/d2a548598be01649e2d46231d151a6c56d10b964d94043a335ae56ea2d92/flatbuffers-25.12.19-py2.py3-none-any.whl --output /work/wheels/flatbuffers-25.12.19-py2.py3-none-any.whl \
    && echo '7634f50c427838bb021c2d66a3d1168e9d199b0607e6329399f04846d42e20b4  /work/wheels/flatbuffers-25.12.19-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/58/a2/bb081bab032533a855d44de1d56f8e8426114ff1ba5d1f07a438a0a654f8/idna-3.20-py3-none-any.whl --output /work/wheels/idna-3.20-py3-none-any.whl \
    && echo 'ab7ae7122974553370f0bdb919e1a960b2cd1bc1ef0276416d896db81c14582c  /work/wheels/idna-3.20-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/93/eb/24d94db0530029649b266ec3ca8221c07f2754f56046181f13237d2518f5/magika-1.0.3-py3-none-any.whl --output /work/wheels/magika-1.0.3-py3-none-any.whl \
    && echo '938d8e033953f2ddeb8c35dc423aa289ca116bfa7a71a778f6e77460f9025803  /work/wheels/magika-1.0.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/04/10/fa543d484e8b1199243fe20eedd02cc5af050edebce98a7293a5773df592/markdownify-1.2.3-py3-none-any.whl --output /work/wheels/markdownify-1.2.3-py3-none-any.whl \
    && echo 'a189a0bedfd14009030fde5f85bb6f77c56897cb839b5c25315dd7d4e3e290ba  /work/wheels/markdownify-1.2.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/aa/74/a891a659ccc427469de0d7bdbd5ff770a35f73084ee590ce02456cf61f7f/onnxruntime-1.31.1-cp314-cp314-manylinux_2_28_x86_64.whl --output /work/wheels/onnxruntime-1.31.1-cp314-cp314-manylinux_2_28_x86_64.whl \
    && echo 'c20d7f15d84427db070b163f78c2c7146cc93edd6113fa7327671259a24184fe  /work/wheels/onnxruntime-1.31.1-cp314-cp314-manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/63/34/ba1c580383c9eada3711951fef0795c80b829a078d72188184bcab9dd527/packaging-26.3-py3-none-any.whl --output /work/wheels/packaging-26.3-py3-none-any.whl \
    && echo 'd7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c  /work/wheels/packaging-26.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e4/04/d52c7016b04b6c5108f26691f9d33ec82a9b65d041f1a9c771137693d618/protobuf-7.36.2-py3-none-any.whl --output /work/wheels/protobuf-7.36.2-py3-none-any.whl \
    && echo 'bdb3a345d48db958e6ce1f18e508beb0cc981d64f24088427549c866cd039f1e  /work/wheels/protobuf-7.36.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a0/f4/c67b0b3f1b9245e8d266f0f112c500d50e5b4e83cb6f3b71b6528104182a/requests-2.34.2-py3-none-any.whl --output /work/wheels/requests-2.34.2-py3-none-any.whl \
    && echo '2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0  /work/wheels/requests-2.34.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b7/ce/149a00dd41f10bc29e5921b496af8b574d8413afcd5e30dfa0ed46c2cc5e/six-1.17.0-py2.py3-none-any.whl --output /work/wheels/six-1.17.0-py2.py3-none-any.whl \
    && echo '4721f391ed90541fddacab5acf947aa0d3dc7d27b2e1e8eda2be8970586c3274  /work/wheels/six-1.17.0-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/88/73/6a2087c72975cfc07394623bca8d17654342ea4055ae368deafe5a81a542/soupsieve-4.1-py3-none-any.whl --output /work/wheels/soupsieve-4.1-py3-none-any.whl \
    && echo 'e4d667b3974ce6e038e7390486b8093369854a1d345ffdd4c121dfc4a782e809  /work/wheels/soupsieve-4.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl --output /work/wheels/typing_extensions-4.16.0-py3-none-any.whl \
    && echo '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  /work/wheels/typing_extensions-4.16.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/92/9d/c4e665119135114480843e7ab388fa94d8480650450e6f8e26b70d323a4c/urllib3-2.8.0-py3-none-any.whl --output /work/wheels/urllib3-2.8.0-py3-none-any.whl \
    && echo '0cf3cae568d36aa9576b28dfb35f11328f1cb974ca7647d9475ebb86c75ac6e3  /work/wheels/urllib3-2.8.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e9/02/4e7d553a7ac4b4238b38b3c1b80d486e9d4436f8d2acbf87a0997fe3f402/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo 'b0431303acaea1089ad4b3e9ce4e6518193def1118d4073ca848635ee4ea2e96  /work/wheels/cffi-2.1.1-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/fc/ad/d07d7862a62ffa6d79d68074d14823243dd235a77c45262acbf6adeb28bf/charset_normalizer-3.5.2-py3-none-any.whl --output /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl \
    && echo 'b6b751274acb69d77b3323d6b7dbaa3c7fdfc1eb829b7eb61d262f32e1af9685  /work/wheels/charset_normalizer-3.5.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/21/69/64cef1f702bf6657e0cc186ed1a2891d50d29fb41586b254e1c07adea261/cryptography-50.0.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/cryptography-50.0.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '630ebfea3bf689d075f82316324ff7433dc447fe6bc1bfc76524b74b4a9567d2  /work/wheels/cryptography-50.0.2-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/20/8b/28c4eaec9d6b036a52cb44720408f26b1a143ca9bce76cc19e8f5de00ab4/pdfminer_six-20260107-py3-none-any.whl --output /work/wheels/pdfminer_six-20260107-py3-none-any.whl \
    && echo '366585ba97e80dffa8f00cebe303d2f381884d8637af4ce422f1df3ef38111a9  /work/wheels/pdfminer_six-20260107-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a2/9a/07d658e1e7fad860f1c541ab941348125dbdab773be3a0afaf32361866c7/pdfplumber-0.11.10-py3-none-any.whl --output /work/wheels/pdfplumber-0.11.10-py3-none-any.whl \
    && echo '7741ea81bf165b474b153e6789d10d18e06b6ddcf3ec84289c3ef2fed6802580  /work/wheels/pdfplumber-0.11.10-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/1d/f2/1371707ce438ba9a43f9d24089828494ec6f9396e28cd7903aa704dd6306/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'e91c2b1cbeae768c98752e67e717e283d68dae45717b41f2d91eaee648e37b7d  /work/wheels/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b6/ae/315bbeee126a769cbde43cf4908acb4b40408d8bf8bbf334dd7368d8dadf/pycparser-3.12-py3-none-any.whl --output /work/wheels/pycparser-3.12-py3-none-any.whl \
    && echo 'a076f3f489b39b43ed13563a1dafe42447445bec2e294154ec5c57fcdda4c85e  /work/wheels/pycparser-3.12-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/bf/8c/4d5804eca598bbe894e0a9a510807e221c1623e7276ce6b68fa2660dc933/pypdfium2-5.10.1-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl --output /work/wheels/pypdfium2-5.10.1-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    && echo '3ba127750bc3f4161461538d532d74491cd976f584f1753a6cee9cb821338ec1  /work/wheels/pypdfium2-5.10.1-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show markitdown atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
