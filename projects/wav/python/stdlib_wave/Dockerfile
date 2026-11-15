FROM --platform=linux/amd64 python@sha256:4888fbac5737c749d34214356d2350ec0faa1c9df871fec5fe420d38085b0e7d

WORKDIR /work
RUN echo '8939d69fc655cd3eabedfc1684f09c43942e08bcf82fb91f64b8b0b8651d37b5  /usr/local/lib/python3.13/wave.py' | sha256sum --check
ADD --checksum=sha256:f8a9f51ce8369026e8eb7b7174835e8c4c85a1a6db5d9add36c15100779d2a39 \
    https://files.pythonhosted.org/packages/4e/18/e19718c384fd7d801d0da7485407daef9af6194b6d8c8818175bec5efec6/atheris-3.1.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    /tmp/wheels/atheris-3.1.0-cp313-cp313-manylinux2014_x86_64.manylinux_2_17_x86_64.whl
RUN pip install --no-index --no-deps /tmp/wheels/*.whl \
    && rm -rf /tmp/wheels /root/.cache/pip \
    && { python --version; pip show atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt
COPY harness.py fuzz.py run-control.py /work/
ENTRYPOINT ["/usr/local/bin/python", "/work/run-control.py"]
