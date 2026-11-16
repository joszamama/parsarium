FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/53/01/7171d610728d559292b8a3174ad26894592989fefcfdd929ebe05c73e7f3/tp_http_request_response_parser-2026.5.18-py3-none-any.whl --output /work/wheels/tp_http_request_response_parser-2026.5.18-py3-none-any.whl \
    && echo '9e0daf9e30d7fdaf446a7be9a04e36b7d7a756ee3d831870afebaba3a8c200e3  /work/wheels/tp_http_request_response_parser-2026.5.18-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/44/bf/088a9fe9f894f29bc363956281b9a4362520b926d74b59863e8c8d17d583/json_duplicate_keys-2026.5.18-py3-none-any.whl --output /work/wheels/json_duplicate_keys-2026.5.18-py3-none-any.whl \
    && echo '85b44fc58c4905519345aafae1881f717785051d66b443a6c836e3d4fc1edd02  /work/wheels/json_duplicate_keys-2026.5.18-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/78/1e/a4347017dba6c8722420b5f6357c3d23bb5a169d117e4259e5758e2845c4/tp_generator-2026.5.18-py3-none-any.whl --output /work/wheels/tp_generator-2026.5.18-py3-none-any.whl \
    && echo '390aceb8be58167a21a24c7ed2baea9888aa2b471a1b4e65d8b1bb254607008c  /work/wheels/tp_generator-2026.5.18-py3-none-any.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show tp-http-request-response-parser atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
