FROM --platform=linux/amd64 ubuntu@sha256:73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv python3-setuptools python3-wheel \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/11/7a/0b72860fa195a2f506698201c7e0f11a7f74bc4e46d42257706af342c749/point_cloud_utils-0.34.0.tar.gz --output /work/wheels/point_cloud_utils-0.34.0.tar.gz \
    && echo '922f326f4c3058cb0b48b32105fb979edb048cb4b8e4f371e92c040365b130c5  /work/wheels/point_cloud_utils-0.34.0.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/26/bc/4869442f54ed3e99cc6fc10d8b1d677f41fc53a8802f7857d9005740b330/point_cloud_utils-0.34.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl --output /work/wheels/point_cloud_utils-0.34.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    && echo '58aca1db983397822046ec69c596d1d6315794af862d20320313857a192a9913  /work/wheels/point_cloud_utils-0.34.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/0a/88/fd6ad595dafa9c7ce56dbfcaff0c7244988dac3af86c771166c6516ccf6b/atheris-3.1.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo 'ec5e11f21a4c197fe91f7aea2b2de88e623c73a21fc07b105ac6329a1588457b  /work/wheels/atheris-3.1.0-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/43/a3/c799c62e19c337e6d3770b08e475887fb30ce8477d3c09efca6b2f0228a6/numpy-2.5.4-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/numpy-2.5.4-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'fbde6962867ee75b48b0ee29b2b9372ec5d617799dbaf38e82dc0596f2f7738a  /work/wheels/numpy-2.5.4-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/df/64/ff35eb9e54894cf471ff4716abd3c81eb0a0626869217ce3e6ba4ccf17d7/scipy-1.18.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl --output /work/wheels/scipy-1.18.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl \
    && echo 'f55fa87b6c612ecd6b058f167c53231b1d14e412efe361d3d6e38b3631c73218  /work/wheels/scipy-1.18.1-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
RUN { python3 --version; /opt/venv/bin/pip show point-cloud-utils atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:73b999393d07f2bf65a40373778a44dc9a6d54ad7718d29247d8ff9413c4d6a8
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.py harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
