FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/61/57/a92037304a92496a1bf735d7549d635b8569412209cac7c16e27bbe4e7ac/svglab-0.18.0-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/svglab-0.18.0-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '21ca7aa49d5bcb1087a56f5f7d8b0f6de4659f957355f105de3a79be52d904b5  /work/wheels/svglab-0.18.0-cp311-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/99/91/8acff4f5e50511b911bbccb72b8628a49c68ce14148cd9f6431094859a90/annotated_types-0.8.0-py3-none-any.whl --output /work/wheels/annotated_types-0.8.0-py3-none-any.whl \
    && echo 'f072f4d804ea359e4eaf198b1af7a8b0943881a87f31bb764f8bf219bb9419e0  /work/wheels/annotated_types-0.8.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/88/c6/92fcd42f1ba33e1184263f25bfabf3d27c383410470f169e4b8163bf9c17/beautifulsoup4-4.15.0-py3-none-any.whl --output /work/wheels/beautifulsoup4-4.15.0-py3-none-any.whl \
    && echo 'd6f88de62e1d4e38ecb1077eb9724cd0eff29d2a08ca16a401e9b9e93f117cf9  /work/wheels/beautifulsoup4-4.15.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/97/53/2a3c7d562271ec6b6e38e7216b3104899f8aa4180c0713cb8aaf69e29cd5/bidict-0.24.1-py3-none-any.whl --output /work/wheels/bidict-0.24.1-py3-none-any.whl \
    && echo 'fd3eaa737917d8a14f4baa391670c433c4e3f6f5fd2cd99d4bf436437f432364  /work/wheels/bidict-0.24.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/82/3d/14ce75ef66813643812f3093ab17e46d3a206942ce7376d31ec2d36229e7/lark-1.3.1-py3-none-any.whl --output /work/wheels/lark-1.3.1-py3-none-any.whl \
    && echo 'c629b661023a014c37da873b4ff58a817398d12635d3bbb2c5a03be7fe5d1e12  /work/wheels/lark-1.3.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/66/bc/6230cf80e4331c33383b0b6b73dc31a393dd76edd4cb73d761de5123034d/lxml-6.1.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/lxml-6.1.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo 'c6c0c13128a32eb04a51357e56a094e13aa8e6d3d1884de2e9ae923f6915e1a8  /work/wheels/lxml-6.1.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/5d/57/3c4b1c6f2e0cc29ba023802458ea3d2a996f87085559e4a5f2192d549532/more_itertools-11.2.1-py3-none-any.whl --output /work/wheels/more_itertools-11.2.1-py3-none-any.whl \
    && echo '35a7377edd1dd6608dcb2cdf534ded55ea32d49448875ad042cd3f879fb1ded0  /work/wheels/more_itertools-11.2.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/1d/f2/1371707ce438ba9a43f9d24089828494ec6f9396e28cd7903aa704dd6306/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'e91c2b1cbeae768c98752e67e717e283d68dae45717b41f2d91eaee648e37b7d  /work/wheels/pillow-13.0.0-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/72/b8/b864503789ef5c58597d2a7b4adbee62c26440ab1e682581fc6838df8947/pydantic-2.14.3-py3-none-any.whl --output /work/wheels/pydantic-2.14.3-py3-none-any.whl \
    && echo '3f7b347782ab7e4cf4c798496ae3a82787d9f21ec12676a9c564355eeef8daa8  /work/wheels/pydantic-2.14.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/56/9c/621ad8f88590a92a086b1168dce09369d9c5e079e2e635e6646d248af55b/pydantic_core-2.50.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/pydantic_core-2.50.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo 'f1d62fb172db35c6478c9323da34ff37d1f3d37d7d44337a9d94ba8c583e5730  /work/wheels/pydantic_core-2.50.4-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/17/c1/3226e6d7f5a4f736f38ac11a6fbb262d701889802595cdb0f53a885ac2e0/pydantic_extra_types-2.11.1-py3-none-any.whl --output /work/wheels/pydantic_extra_types-2.11.1-py3-none-any.whl \
    && echo '1722ea2bddae5628ace25f2aa685b69978ef533123e5638cfbddb999e0100ec1  /work/wheels/pydantic_extra_types-2.11.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ff/9a/9afaade874b2fa6c752c36f1548f718b5b83af81ed9b76628329dab81c1b/rfc3986-2.0.0-py2.py3-none-any.whl --output /work/wheels/rfc3986-2.0.0-py2.py3-none-any.whl \
    && echo '50b1502b60e289cb37883f3dfd34532b8873c7de9f49bb546641ce9cbd256ebd  /work/wheels/rfc3986-2.0.0-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/88/73/6a2087c72975cfc07394623bca8d17654342ea4055ae368deafe5a81a542/soupsieve-4.1-py3-none-any.whl --output /work/wheels/soupsieve-4.1-py3-none-any.whl \
    && echo 'e4d667b3974ce6e038e7390486b8093369854a1d345ffdd4c121dfc4a782e809  /work/wheels/soupsieve-4.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl --output /work/wheels/typing_extensions-4.16.0-py3-none-any.whl \
    && echo '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  /work/wheels/typing_extensions-4.16.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/de/0c/ea2544850a7c135e15033a5c7a8e7211136184b7ae63e2239d557c2b3019/typing_inspection-0.4.5-py3-none-any.whl --output /work/wheels/typing_inspection-0.4.5-py3-none-any.whl \
    && echo 'bc210535442b39e1bf2805e0c7a17dfd6a4ace760c84c7f7d16245d23a6b1c39  /work/wheels/typing_inspection-0.4.5-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/13/23/c194fd6c6258727f694e22b106c262c7d2678049dbc2d2045743e235f43a/useful_types-0.2.1-py3-none-any.whl --output /work/wheels/useful_types-0.2.1-py3-none-any.whl \
    && echo '0dca32763d7271b5c8c7c395c44c10d09dba47a41aec97dcb085041ad096e0e9  /work/wheels/useful_types-0.2.1-py3-none-any.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show svglab atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
