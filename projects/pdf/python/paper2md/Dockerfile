FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/3b/63/2b5e81e0a8ed768667c7a2866a9da8f9053858ef665401a865318870d6a6/paper2md-0.1.0-py3-none-any.whl --output /work/wheels/paper2md-0.1.0-py3-none-any.whl \
    && echo 'db2ce64a0a0992c838f4a5d68e7fbd46f6a85c754f236afc922d13793812ecdd  /work/wheels/paper2md-0.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/cd/f5/3dd85d583e55be76cd02b1fc9bbec771b12d63124b01661d9535ccf8721f/annotated_doc-0.0.6-py3-none-any.whl --output /work/wheels/annotated_doc-0.0.6-py3-none-any.whl \
    && echo '361ca0950cc7082f53fa69e9328409f40a62c61e57e0a47e1825a08078a58a53  /work/wheels/annotated_doc-0.0.6-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/99/91/8acff4f5e50511b911bbccb72b8628a49c68ce14148cd9f6431094859a90/annotated_types-0.8.0-py3-none-any.whl --output /work/wheels/annotated_types-0.8.0-py3-none-any.whl \
    && echo 'f072f4d804ea359e4eaf198b1af7a8b0943881a87f31bb764f8bf219bb9419e0  /work/wheels/annotated_types-0.8.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e8/2d/d2a548598be01649e2d46231d151a6c56d10b964d94043a335ae56ea2d92/flatbuffers-25.12.19-py2.py3-none-any.whl --output /work/wheels/flatbuffers-25.12.19-py2.py3-none-any.whl \
    && echo '7634f50c427838bb021c2d66a3d1168e9d199b0607e6329399f04846d42e20b4  /work/wheels/flatbuffers-25.12.19-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c9/31/5f0ac2f1a1c67423c995c731a11cd4ad05d081a2be969d74f868bdb9cc70/markdown_it_py-4.3.0-py3-none-any.whl --output /work/wheels/markdown_it_py-4.3.0-py3-none-any.whl \
    && echo '7aa1511a46c39138de78d9eba92ce47e63124d8003fc98b3a351909e04239efa  /work/wheels/markdown_it_py-4.3.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b3/38/89ba8ad64ae25be8de66a6d463314cf1eb366222074cfda9ee839c56a4b4/mdurl-0.1.2-py3-none-any.whl --output /work/wheels/mdurl-0.1.2-py3-none-any.whl \
    && echo '84008a41e51615a49fc9966191ff91509e3c40b939176e643fd50a5c2196b8f8  /work/wheels/mdurl-0.1.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7e/cd/fe58041e9011f307c490e3e17dd48cc516448f7c698a3f2d9d9d65d7e6a8/networkx-3.7-py3-none-any.whl --output /work/wheels/networkx-3.7-py3-none-any.whl \
    && echo 'e3fd2c13a7814cee3746340d8d7f8598a67f16a58bf47fb7f8793fab6efca1b0  /work/wheels/networkx-3.7-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/aa/74/a891a659ccc427469de0d7bdbd5ff770a35f73084ee590ce02456cf61f7f/onnxruntime-1.31.1-cp314-cp314-manylinux_2_28_x86_64.whl --output /work/wheels/onnxruntime-1.31.1-cp314-cp314-manylinux_2_28_x86_64.whl \
    && echo 'c20d7f15d84427db070b163f78c2c7146cc93edd6113fa7327671259a24184fe  /work/wheels/onnxruntime-1.31.1-cp314-cp314-manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/63/34/ba1c580383c9eada3711951fef0795c80b829a078d72188184bcab9dd527/packaging-26.3-py3-none-any.whl --output /work/wheels/packaging-26.3-py3-none-any.whl \
    && echo 'd7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c  /work/wheels/packaging-26.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e4/04/d52c7016b04b6c5108f26691f9d33ec82a9b65d041f1a9c771137693d618/protobuf-7.36.2-py3-none-any.whl --output /work/wheels/protobuf-7.36.2-py3-none-any.whl \
    && echo 'bdb3a345d48db958e6ce1f18e508beb0cc981d64f24088427549c866cd039f1e  /work/wheels/protobuf-7.36.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b5/70/5d8df3b09e25bce090399cf48e452d25c935ab72dad19406c77f4e828045/psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl \
    && echo '076a2d2f923fd4821644f5ba89f059523da90dc9014e85f8e45a5774ca5bc6f9  /work/wheels/psutil-7.2.2-cp36-abi3-manylinux2010_x86_64.manylinux_2_12_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/72/b8/b864503789ef5c58597d2a7b4adbee62c26440ab1e682581fc6838df8947/pydantic-2.14.3-py3-none-any.whl --output /work/wheels/pydantic-2.14.3-py3-none-any.whl \
    && echo '3f7b347782ab7e4cf4c798496ae3a82787d9f21ec12676a9c564355eeef8daa8  /work/wheels/pydantic-2.14.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/56/9c/621ad8f88590a92a086b1168dce09369d9c5e079e2e635e6646d248af55b/pydantic_core-2.50.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/pydantic_core-2.50.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo 'f1d62fb172db35c6478c9323da34ff37d1f3d37d7d44337a9d94ba8c583e5730  /work/wheels/pydantic_core-2.50.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/71/46/17f022dd3e953bf20a04a028a21ec746d942f8d2af30fa0f124fa0e6a684/pygments-2.21.0-py3-none-any.whl --output /work/wheels/pygments-2.21.0-py3-none-any.whl \
    && echo '2363c69b61c4a97c838da3b130dcd6468f4848992b21a82f2a63ec34377137d9  /work/wheels/pygments-2.21.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f4/dc/e244c162ab621a45bfe36e33fe432264ef7e40592f739474864df66a2dd8/pymupdf-2.1-cp311-abi3-manylinux_2_28_x86_64.whl --output /work/wheels/pymupdf-2.1-cp311-abi3-manylinux_2_28_x86_64.whl \
    && echo 'a9efa2e9e5f469d3b5749199329739cfef1ff1d1846538ced4885c544eecbcd9  /work/wheels/pymupdf-2.1-cp311-abi3-manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e4/13/7a1edc4029348e728114cf37837dd121a7439defd668caa087d128b5df2d/pymupdf_layout-2.1-py3-none-any.whl --output /work/wheels/pymupdf_layout-2.1-py3-none-any.whl \
    && echo 'e7e00bc50ec9113d36bdbb0dd5cdafa5f4d61e22e598960fc187ee4f721f5095  /work/wheels/pymupdf_layout-2.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/38/19/21e262de4e1ddbcd552889e5f04147f83ed219dd13d1e0e0db46ab4d2347/pymupdf4llm-2.1-py3-none-any.whl --output /work/wheels/pymupdf4llm-2.1-py3-none-any.whl \
    && echo '2fe8bb344444c6a8ef41fd745d2d10f6da59df6e104ef20f35d51dd26914b5fb  /work/wheels/pymupdf4llm-2.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/88/f9/16491d7ed2a919954993e48aa941b200f38040928474c9e85ea9e64222c3/pyyaml-6.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/pyyaml-6.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'c458b6d084f9b935061bc36216e8a69a7e293a2f1e68bf956dcd9e6cbcd143f5  /work/wheels/pyyaml-6.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/82/3b/64d4899d73f91ba49a8c18a8ff3f0ea8f1c1d75481760df8c68ef5235bf5/rich-15.0.0-py3-none-any.whl --output /work/wheels/rich-15.0.0-py3-none-any.whl \
    && echo '33bd4ef74232fb73fe9279a257718407f169c09b78a87ad3d296f548e27de0bb  /work/wheels/rich-15.0.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e0/f9/0595336914c5619e5f28a1fb793285925a8cd4b432c9da0a987836c7f822/shellingham-1.5.4-py2.py3-none-any.whl --output /work/wheels/shellingham-1.5.4-py2.py3-none-any.whl \
    && echo '7ecfff8f2fd72616f7481040475a65b2bf8af90a56c89140852d1120324e8686  /work/wheels/shellingham-1.5.4-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/99/55/db07de81b5c630da5cbf5c7df646580ca26dfaefa593667fc6f2fe016d2e/tabulate-0.10.0-py3-none-any.whl --output /work/wheels/tabulate-0.10.0-py3-none-any.whl \
    && echo 'f0b0622e567335c8fabaaa659f1b33bcb6ddfe2e496071b743aa113f8774f2d3  /work/wheels/tabulate-0.10.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/05/ff/51969745f31cea6bcd12151e668febcf979656316e67a7755942267c1273/typer-0.29.1-py3-none-any.whl --output /work/wheels/typer-0.29.1-py3-none-any.whl \
    && echo '00dbc549c13428bec1be55fe1f4d0fb8c6637a310e4f178ef14abe9534ee7b58  /work/wheels/typer-0.29.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl --output /work/wheels/typing_extensions-4.16.0-py3-none-any.whl \
    && echo '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  /work/wheels/typing_extensions-4.16.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/de/0c/ea2544850a7c135e15033a5c7a8e7211136184b7ae63e2239d557c2b3019/typing_inspection-0.4.5-py3-none-any.whl --output /work/wheels/typing_inspection-0.4.5-py3-none-any.whl \
    && echo 'bc210535442b39e1bf2805e0c7a17dfd6a4ace760c84c7f7d16245d23a6b1c39  /work/wheels/typing_inspection-0.4.5-py3-none-any.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show paper2md atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
