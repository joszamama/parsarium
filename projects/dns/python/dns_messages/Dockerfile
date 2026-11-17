FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# dns-messages 1.0.1: pure-Python py3-none-any wheel; its dns_messages/ package must match the sdist byte for byte.
RUN mkdir /work/wheels /work/dnsmsg-sdist /work/dnsmsg-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/35/8b/764359c69062c895a149d7d43db06faf08ae42542fe43a8d01594d264d9d/dns_messages-1.0.1-py3-none-any.whl --output /work/wheels/dns_messages-1.0.1-py3-none-any.whl \
    && echo '680a84adbb85aacefe35778041b0afec01caeba66aa3ccb7863086242f20cb59  /work/wheels/dns_messages-1.0.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ee/4d/00f225f63ed2c239b956c8f882b71c979f3c28c437d3467dad90593a531c/dns-messages-1.0.1.tar.gz --output /work/dnsmsg-sdist.tar.gz \
    && echo 'dcc959efb78c6685ba079a0cef586f3e4619be48ae1332c0611681b39212285b  /work/dnsmsg-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/dnsmsg-sdist.tar.gz --strip-components=1 -C /work/dnsmsg-sdist \
    && unzip -q /work/wheels/dns_messages-1.0.1-py3-none-any.whl -d /work/dnsmsg-wheel \
    && diff -r /work/dnsmsg-sdist/dns_messages /work/dnsmsg-wheel/dns_messages \
    && grep -F 'Classifier: License :: OSI Approved :: MIT License' /work/dnsmsg-wheel/dns_messages-1.0.1.dist-info/METADATA \
    && ! grep -q '^Requires-Dist:' /work/dnsmsg-wheel/dns_messages-1.0.1.dist-info/METADATA \
    && cd /work/dnsmsg-wheel \
    && printf '%s\n' \
       '84ea70c56ccf63b0da0e7f6bb537d209ec29a8f736216d210d1cc5fc80c3dd16  dns_messages/dns_objects/dns_message_parser.py' \
       '675fd1f02271b4e2d6a04ae57fba7a6825852b1fd9d225bebf629f843dec83ee  dns_messages/dns_objects/dns_message.py' \
       'ff50ab9bb2540f47e9b59da247ffba4a2b2e44b123a36004c19f0011dc461fbb  dns_messages/utilities/name_encoder_and_decoder.py' \
       'a28306b5421a18a7965e17cb16f3ff9cf226533c864599476579c79130d97faf  dns_messages-1.0.1.dist-info/LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/dnsmsg-wheel/dns_messages /opt/venv/lib/python3.14/site-packages/dns_messages \
    && /opt/venv/bin/python -c 'import dns_messages, importlib.metadata as m; assert m.version("dns-messages") == "1.0.1"' \
    && { python3 --version; /opt/venv/bin/pip show dns-messages atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum dns_messages/dns_objects/dns_message_parser.py dns_messages/dns_objects/dns_message.py dns_messages/utilities/name_encoder_and_decoder.py; } > /work/toolchain.txt

FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
