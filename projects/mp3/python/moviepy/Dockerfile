FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/9a/73/7d3b2010baa0b5eb1e4dfa9e4385e89b6716be76f2fa21a6c0fe34b68e5a/moviepy-2.2.1-py3-none-any.whl --output /work/wheels/moviepy-2.2.1-py3-none-any.whl \
    && echo '6b56803fec2ac54b557404126ac1160e65448e03798fa282bd23e8fab3795060  /work/wheels/moviepy-2.2.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/05/7f/798705f5296a58ca505d600456748d1be48078eac8a7050d8a98bc9edb89/decorator-5.3.1-py3-none-any.whl --output /work/wheels/decorator-5.3.1-py3-none-any.whl \
    && echo 'f47fe6fdbd2edd623ecfe36875d37aba411624e2670dd395dddae1358689bb3c  /work/wheels/decorator-5.3.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7d/8a/3b7f62b9df56460959f1b9bef094248d2a4d7f393c5b0d2da8efcdf0e40e/imageio-2.38.1-py3-none-any.whl --output /work/wheels/imageio-2.38.1-py3-none-any.whl \
    && echo '36d23eb7423d2fb63f637098758edb3d2df3687f7125e0a5ce8596572022dcf9  /work/wheels/imageio-2.38.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/de/0f/49292fbef69ee10ebcf97bb741602521caafcc6966d5fa1a2b868cc15655/imageio_ffmpeg-0.8.1-py3-none-manylinux_2_28_x86_64.whl --output /work/wheels/imageio_ffmpeg-0.8.1-py3-none-manylinux_2_28_x86_64.whl \
    && echo '050d6850601c3b3890bd2b28306f3b842b3daea390a561101174375a1c460bda  /work/wheels/imageio_ffmpeg-0.8.1-py3-none-manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/16/d5/928078d2b28f26829b138b4a6c3980045022fb409f570657a224ae60ef4e/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'd549420b8858885cea8838a727842249218b9c1da24dd517e25c9c7a948310a3  /work/wheels/numpy-2.5.4-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b5/3d/b932bb4225c80b58dfadaca9d42d08d0b7064d2d1791b6a237f87f661834/pillow-11.3.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/pillow-11.3.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '2465a69cf967b8b49ee1b96d76718cd98c4e925414ead59fdf75cf0fd07df673  /work/wheels/pillow-11.3.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c1/1b/f7ea6cde25621cd9236541c66ff018f4268012a534ec31032bcb187dc5e7/proglog-0.1.12-py3-none-any.whl --output /work/wheels/proglog-0.1.12-py3-none-any.whl \
    && echo 'ccaafce51e80a81c65dc907a460c07ccb8ec1f78dc660cfd8f9ec3a22f01b84c  /work/wheels/proglog-0.1.12-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/60/d1/38f3a3405989a89ac18390803e70c6ad7c7760da4f9b83cbeca0c44a0c72/python_dotenv-1.2.4-py3-none-any.whl --output /work/wheels/python_dotenv-1.2.4-py3-none-any.whl \
    && echo '42269a8a5b3fd54ffa6f3d84b18abed50064717576b4ecf03dc4a55d8aa04fdc  /work/wheels/python_dotenv-1.2.4-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a7/03/921a3d3c75785aca9ebfbfcabfbc3a1be12e2ab5265deb026d55a5a3f83e/tqdm-4.70.1-py3-none-any.whl --output /work/wheels/tqdm-4.70.1-py3-none-any.whl \
    && echo 'c293e525e6fef9c20e8728fd4612df02a0aa31bb5fe91ecd93e123b1b7bffa73  /work/wheels/tqdm-4.70.1-py3-none-any.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show moviepy atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
