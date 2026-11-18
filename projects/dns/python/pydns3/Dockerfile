FROM --platform=linux/amd64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# pydns3 0.0.10 and its struct library pystructs3 0.0.8: pure-Python py3-none-any wheels whose packages must match
# the sdists byte for byte. Only the dependencies that the message codec imports are installed (see manifest).
RUN mkdir /work/wheels /work/pydns-sdist /work/pydns-wheel /work/pystructs-sdist /work/pystructs-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/70/d7/1e190bcbbfd14fe3774b184c72eaabcb6c9a2a6ae9ec94dc301b141d2acb/pydns3-0.0.10-py3-none-any.whl --output /work/wheels/pydns3-0.0.10-py3-none-any.whl \
    && echo '63b811a301edc8f1d3ac0db95bd4140c469418e1dfd8945653c1322e8e74debf  /work/wheels/pydns3-0.0.10-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f3/9a/fdefc2bff9c7af6ffb9d27d250c8475781003ceaca1d71a22ab277230e3a/pystructs3-0.0.8-py3-none-any.whl --output /work/wheels/pystructs3-0.0.8-py3-none-any.whl \
    && echo 'cc2fddff4bbe3656e452c2f2c9e3549139618084b828e8f4eeba1c81fef1c078  /work/wheels/pystructs3-0.0.8-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/86/d7/af8b71eb978f7e256ba22e16750bb91cd3e034b38e31e65420a48b2c7f9d/pyderive3-0.0.8-py3-none-any.whl --output /work/wheels/pyderive3-0.0.8-py3-none-any.whl \
    && echo 'edba3257a709fc2e911caf1e2214633a8583c46fa6aece604e232f4c29663664  /work/wheels/pyderive3-0.0.8-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl --output /work/wheels/typing_extensions-4.16.0-py3-none-any.whl \
    && echo '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  /work/wheels/typing_extensions-4.16.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c3/ff/ae7a5bfe99033e510bea4ed09934e636d93777317a48147369bc0dc2b71f/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl --output /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl \
    && echo '315a0b5c819852b1ffe1ca72efc389c7724881f2c33e4aacb8c6bcec49bd5011  /work/wheels/atheris-3.1.0-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/84/26/09ab28c9deb27a58f95d652bf813b29a1ff0d5da7974050a002b74e4690a/pydns3-0.0.10.tar.gz --output /work/pydns-sdist.tar.gz \
    && echo 'c33402db6e0e6ad2076790c1aa621eb3e9dca807c6e96d7f52d5de03f2dda5a2  /work/pydns-sdist.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b9/fb/90102ce0d1de7ee86c299a1723bcf0f7628ba83434d16f89e39bdd77b4da/pystructs3-0.0.8.tar.gz --output /work/pystructs-sdist.tar.gz \
    && echo '4b0bda4f6258c118441dab2f5d87af076bd87b087bac3d170e7f66e76917f928  /work/pystructs-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/pydns-sdist.tar.gz --strip-components=1 -C /work/pydns-sdist \
    && tar -xzf /work/pystructs-sdist.tar.gz --strip-components=1 -C /work/pystructs-sdist \
    && unzip -q /work/wheels/pydns3-0.0.10-py3-none-any.whl -d /work/pydns-wheel \
    && unzip -q /work/wheels/pystructs3-0.0.8-py3-none-any.whl -d /work/pystructs-wheel \
    && diff -r /work/pydns-sdist/pydns /work/pydns-wheel/pydns \
    && diff -r /work/pystructs-sdist/pystructs /work/pystructs-wheel/pystructs \
    && grep -Fx 'Classifier: License :: OSI Approved :: MIT License' /work/pydns-wheel/pydns3-0.0.10.dist-info/METADATA \
    && grep -Fx 'Classifier: License :: OSI Approved :: MIT License' /work/pystructs-wheel/pystructs3-0.0.8.dist-info/METADATA \
    && cd /work/pydns-wheel \
    && printf '%s\n' \
       '0b15afb2c99f80e4b6a0c31222eaeeb344ef9d7a862987b8157daf3693f37081  pydns/message.py' \
       'b7092462e188ede13834796e27582aead4a4affa348ad63fd419ef0ae01447f6  pydns/answer.py' \
       '41014a66a849cb1e5999eb589d38057c31f9da3f41818ba64d8c756c318b5955  pydns/content.py' \
       'b6dc8ea7bce28afac47a6611f379c2cc1640167a1df967d758ef930e372113f7  pydns/flags.py' \
       'a334434225d932ffbf16cb8ff75092a6f4922b18ab2ebaff099aa6ec8e6d1226  pydns/question.py' \
       'e6b7a7d9c56589dd0e0dfa51681f8f65395f96ea2422f41b6130856c2cb0a980  pydns3-0.0.10.dist-info/LICENSE' \
       | sha256sum --check \
    && cd /work/pystructs-wheel \
    && printf '%s\n' \
       'c70074450510d79b73e45b0ab8c4bbdeffcbcbdc3f2719e4fea3624da6682d90  pystructs/abc.py' \
       'ecfa250297bf0ce19ee4d4daf45b263305cd4e46fa4cda47be03b86de28b7769  pystructs/std.py' \
       '36eedaf4b358ee90fae5516e7b5f30cf25888f95c6acf7251271b2a538dca92c  pystructs/struct.py' \
       '233e313d318fe65fafbd238950c0f724a38a5bea653195798425205d68e3dd53  pystructs/net.py' \
       'e6b7a7d9c56589dd0e0dfa51681f8f65395f96ea2422f41b6130856c2cb0a980  pystructs3-0.0.8.dist-info/LICENSE' \
       | sha256sum --check
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/pydns-wheel/pydns /opt/venv/lib/python3.14/site-packages/pydns \
    && diff -r --exclude=__pycache__ /work/pystructs-wheel/pystructs /opt/venv/lib/python3.14/site-packages/pystructs \
    && /opt/venv/bin/python -c 'import pydns, importlib.metadata as m; assert m.version("pydns3") == "0.0.10"' \
    && { python3 --version; /opt/venv/bin/pip show pydns3 pystructs3 pyderive3 typing-extensions atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum pydns/message.py pydns/answer.py pydns/content.py pystructs/std.py pystructs/struct.py; } > /work/toolchain.txt

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
