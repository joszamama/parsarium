FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# sqlfluff 4.5.0: pure-Python py3-none-any wheel; its sqlfluff/ package must match the sdist src/sqlfluff byte for byte.
# Runtime dependencies are pinned wheels; the optional sqlfluffrs (Rust) extra is not installed.
RUN mkdir /work/wheels /work/sqlfluff-sdist /work/sqlfluff-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/4d/32/5a952b376c00dda01465b396958a8985916d9a9293a772d6bda2c37f2cc5/chardet-7.7.0-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl --output /work/wheels/chardet-7.7.0-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl \
    && echo 'a05667635c0496dab47eca8c845c044d1da6d74d34a9bf687199c9c53a38119d  /work/wheels/chardet-7.7.0-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/31/7d/164b7ffc8624fe9efb4221bf9af485d5c1e41b9ae118045d2b6dc5457d8b/click-8.5.1-py3-none-any.whl --output /work/wheels/click-8.5.1-py3-none-any.whl \
    && echo '8bb5376d2006950386f8c6427613334a2acadc5f559cb80e638d00b4df957e37  /work/wheels/click-8.5.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/d1/d6/3965ed04c63042e047cb6a3e6ed1a63a35087b6a609aa3a15ed8ac56c221/colorama-0.4.6-py2.py3-none-any.whl --output /work/wheels/colorama-0.4.6-py2.py3-none-any.whl \
    && echo '4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6  /work/wheels/colorama-0.4.6-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e9/2f/ed55dbc0fb7e7458c2f8e7b5502239308164df92986c8b6f3462f28ff666/diff_cover-11.0.3-py3-none-any.whl --output /work/wheels/diff_cover-11.0.3-py3-none-any.whl \
    && echo 'f97cfe094567922e4d7fd063262c5fca36d6325296813dc5814d7439e1c3a733  /work/wheels/diff_cover-11.0.3-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/62/a1/3d680cbfd5f4b8f15abc1d571870c5fc3e594bb582bc3b64ea099db13e56/jinja2-3.1.6-py3-none-any.whl --output /work/wheels/jinja2-3.1.6-py3-none-any.whl \
    && echo '85ece4451f492d0c13c5dd7c13a64681a86afae63a5f347908daf103ce6d2f67  /work/wheels/jinja2-3.1.6-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/9a/a8/73a81135e85ba66217f5af7facb03bbb386807e1a729ab64532e4c802652/markupsafe-3.0.4-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl --output /work/wheels/markupsafe-3.0.4-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl \
    && echo '1caa2fa5a6184fb233153b35f654e6687bd555476f6170f29d8ee9be1a8b0af9  /work/wheels/markupsafe-3.0.4-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f1/d9/7fb5aa316bc299258e68c73ba3bddbc499654a07f151cba08f6153988714/pathspec-1.1.1-py3-none-any.whl --output /work/wheels/pathspec-1.1.1-py3-none-any.whl \
    && echo 'a00ce642f577bf7f473932318056212bc4f8bfdf53128c78bbd5af0b9b20b189  /work/wheels/pathspec-1.1.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f8/46/3737af9f971f3934794103256d7f1ed6200a62be0c7b7ff09ac4cf6b3422/platformdirs-4.14.7-py3-none-any.whl --output /work/wheels/platformdirs-4.14.7-py3-none-any.whl \
    && echo '391513b74707c42335fff3ea17eaac657a7ee9ffcadd809634d34ea594d0122c  /work/wheels/platformdirs-4.14.7-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/40/9e/2b38731e0fc536806f16490e1a12d7f0dc2a1235aa8cc07bcc75416a7daa/pluggy-1.7.0-py3-none-any.whl --output /work/wheels/pluggy-1.7.0-py3-none-any.whl \
    && echo '7dd7b0d8832ba3cb632c306926ded123429211b83641b35dc5c41ad2d34f9bec  /work/wheels/pluggy-1.7.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/71/46/17f022dd3e953bf20a04a028a21ec746d942f8d2af30fa0f124fa0e6a684/pygments-2.21.0-py3-none-any.whl --output /work/wheels/pygments-2.21.0-py3-none-any.whl \
    && echo '2363c69b61c4a97c838da3b130dcd6468f4848992b21a82f2a63ec34377137d9  /work/wheels/pygments-2.21.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/92/b5/47e807c2623074914e29dabd16cbbdd4bf5e9b2db9f8090fa64411fc5382/pyyaml-6.0.3-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl --output /work/wheels/pyyaml-6.0.3-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl \
    && echo '501a031947e3a9025ed4405a168e6ef5ae3126c59f90ce0cd6f2bfc477be31b7  /work/wheels/pyyaml-6.0.3-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/7d/01/67786f8b04bdf3881e1222d78bd78a39633604d332c23e4e3f337b78a683/regex-2026.11.15-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl --output /work/wheels/regex-2026.11.15-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl \
    && echo '99e61a4f575b3439de59de524bed94d144b22a11877407c81c702ce98fb4e1d3  /work/wheels/regex-2026.11.15-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f3/de/78c2f6d023a2dada127baf9a41a7186707d500de89947dd7259d33700bb2/sqlfluff-4.5.0-py3-none-any.whl --output /work/wheels/sqlfluff-4.5.0-py3-none-any.whl \
    && echo '471a9abcad8061e36b69f711a6d89393241e30f9d1e0869f79965c0ae2c889c7  /work/wheels/sqlfluff-4.5.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/02/be/5d2d47b1fb58943194fb59dcf222f7c4e35122ec0ffe8c36e18b5d728f0b/tblib-3.2.2-py3-none-any.whl --output /work/wheels/tblib-3.2.2-py3-none-any.whl \
    && echo '26bdccf339bcce6a88b2b5432c988b266ebbe63a4e593f6b578b1d2e723d2b76  /work/wheels/tblib-3.2.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/a7/03/921a3d3c75785aca9ebfbfcabfbc3a1be12e2ab5265deb026d55a5a3f83e/tqdm-4.70.1-py3-none-any.whl --output /work/wheels/tqdm-4.70.1-py3-none-any.whl \
    && echo 'c293e525e6fef9c20e8728fd4612df02a0aa31bb5fe91ecd93e123b1b7bffa73  /work/wheels/tqdm-4.70.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e6/37/6fa8831fad5ffda6e5d3c2629b4c9ed1a4e480b4d8c9f127f132463d6d75/sqlfluff-4.5.0.tar.gz --output /work/sqlfluff-sdist.tar.gz \
    && echo '0b0d5b2cca03e7d138b8d899249fed5fa54083e407bbd161449c0b30f901b7b8  /work/sqlfluff-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/sqlfluff-sdist.tar.gz --strip-components=1 -C /work/sqlfluff-sdist \
    && unzip -q /work/wheels/sqlfluff-4.5.0-py3-none-any.whl -d /work/sqlfluff-wheel \
    && diff -r /work/sqlfluff-sdist/src/sqlfluff /work/sqlfluff-wheel/sqlfluff \
    && cd /work/sqlfluff-sdist \
    && printf '%s\n' \
       '8f5f76b3c5b0568d8d8a7b7a971bdb8bd450961b695a987f417e259f4ce84c64  src/sqlfluff/core/parser/lexer.py' \
       'f0f840bd11afdf5dcdefcd2229a4ec1e9aed09f522e46fe2fa41899103ac40e3  src/sqlfluff/dialects/dialect_ansi.py' \
       '22dce2dc3663d299ccc2606289647982d757e6157393081e59736a9db335c77f  LICENSE.md' \
       | sha256sum --check \
    && grep -qx 'MIT License' LICENSE.md
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && /opt/venv/bin/pip check \
    && diff -r --exclude=__pycache__ /work/sqlfluff-wheel/sqlfluff /opt/venv/lib/python3.14/site-packages/sqlfluff \
    && /opt/venv/bin/python -c 'import importlib.util, sqlfluff; assert sqlfluff.__version__ == "4.5.0"; assert importlib.util.find_spec("sqlfluffrs") is None; print(list(sqlfluff.parse("SELECT 1", dialect="ansi")))' \
    && { python3 --version; /opt/venv/bin/pip show sqlfluff | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.14/site-packages && sha256sum sqlfluff/core/parser/lexer.py sqlfluff/dialects/dialect_ansi.py; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
