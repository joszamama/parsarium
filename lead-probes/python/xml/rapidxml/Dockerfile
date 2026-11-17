FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl g++ python3 python3-dev python3-venv python3-setuptools \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# RapidXml 2.1.4 is published as an sdist only; it bundles the RapidXML 1.13 headers.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/92/7f/98327f2ca6240190450ab5bc434abecf45c64c7da2bd394a73a8f5fa13d5/rapidxml-2.1.4.tar.gz --output /work/rapidxml-2.1.4.tar.gz \
    && echo 'aae02d75c98c062927d1a5c40f07838c65760b144fd0d7322f097a27a081205d  /work/rapidxml-2.1.4.tar.gz' | sha256sum --check \
    && python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-build-isolation --no-deps /work/rapidxml-2.1.4.tar.gz \
    && /opt/venv/bin/python -c 'import rapidxml, rapidxml.c_ext; print(rapidxml.RapidXml)'
COPY probe.py /work/probe.py
ENTRYPOINT ["/opt/venv/bin/python", "/work/probe.py"]
