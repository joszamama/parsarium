FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# tomli 2.5.0: the pure-Python py3-none-any wheel (not the mypyc-compiled cp3xx wheels); its tomli/ package must match the sdist src/tomli byte for byte.
RUN mkdir /work/wheels /work/tomli-sdist /work/tomli-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/60/3f/3e3f8fd0919249b0200c80fbc4f9a1e70be19f9883da71dfb7f8b9ab8aca/tomli-2.5.0-py3-none-any.whl --output /work/wheels/tomli-2.5.0-py3-none-any.whl \
    && echo '32a7b79ac57a2e83670ce329ccf675798bc5a2094783a63676866b70503f2e2b  /work/wheels/tomli-2.5.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b0/78/9ad63712633ed3ab5cc1a648d863d7e7da371e9425e209555a0fe711b695/tomli-2.5.0.tar.gz --output /work/tomli-sdist.tar.gz \
    && echo '264507556cd8b8c8e7c6ee037cdf443a463f03f4c958e57195e3d369711b8ff6  /work/tomli-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/tomli-sdist.tar.gz --strip-components=1 -C /work/tomli-sdist \
    && unzip -q /work/wheels/tomli-2.5.0-py3-none-any.whl -d /work/tomli-wheel \
    && diff -r /work/tomli-sdist/src/tomli /work/tomli-wheel/tomli \
    && grep -Fx 'License-Expression: MIT' /work/tomli-wheel/tomli-2.5.0.dist-info/METADATA \
    && ! grep -q '^Requires-Dist:' /work/tomli-wheel/tomli-2.5.0.dist-info/METADATA \
    && cd /work/tomli-sdist \
    && printf '%s\n' \
       '3e782f1bc85639ecef630ae686df3d849f2bedd2e9c987d8f5109a5a154df131  src/tomli/_parser.py' \
       'a12359fe294523a72112e434d58452a14c9d050affa2417f9927474e4166bfdd  src/tomli/_re.py' \
       'f864c6d9552a929c7032ace654ee05ef26ca75d21b027b801d77e65907138b74  src/tomli/_types.py' \
       '7182927b251660b7d649eec79e0dcaf03a59973793400990a693d9f6f8b73eca  src/tomli/__init__.py' \
       'b80816b0d530b8accb4c2211783790984a6e3b61922c2b5ee92f3372ab2742fe  LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/tomli-wheel/tomli /opt/venv/lib/python3.14/site-packages/tomli \
    && /opt/venv/bin/python -c 'import tomli; assert tomli.__version__ == "2.5.0"; assert tomli.__file__.endswith("/tomli/__init__.py"); print(tomli.loads("ready = true\n"))' \
    && { python3 --version; /opt/venv/bin/pip show tomli atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum tomli/_parser.py tomli/_re.py tomli/_types.py tomli/__init__.py; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY expected /work/expected
COPY harness.py fuzz.py replay.py structure.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
