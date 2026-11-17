FROM --platform=linux/amd64 ubuntu@sha256:73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b9/f2/d31e6ad42d657af07be2ffd779190353f759a07b51232b9e1d724f2cda46/pygame-2.6.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl --output /work/wheels/pygame-2.6.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    && echo '1206125f14cae22c44565c9d333607f1d9f59487b1f1432945dfc809aeaa3e88  /work/wheels/pygame-2.6.1-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/0a/88/fd6ad595dafa9c7ce56dbfcaff0c7244988dac3af86c771166c6516ccf6b/atheris-3.1.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo 'ec5e11f21a4c197fe91f7aea2b2de88e623c73a21fc07b105ac6329a1588457b  /work/wheels/atheris-3.1.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show pygame atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8
ENV DEBIAN_FRONTEND=noninteractive
ENV PYGAME_HIDE_SUPPORT_PROMPT=1 SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    python3 libstdc++6 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
