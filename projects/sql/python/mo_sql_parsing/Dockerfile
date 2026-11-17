FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl g++ libclang-rt-14-dev python3 python3-dev python3-venv unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# mo-sql-parsing 11.699.26234: pure-Python py3-none-any wheel; its mo_sql_parsing/ package must match the sdist byte for byte.
# The grammar runs on the pinned mo-parsing 9.3.26234 engine with its pinned mo-dots, mo-future and mo-imports helpers.
RUN mkdir /work/wheels /work/mo-sql-parsing-sdist /work/mo-sql-parsing-wheel \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/d5/0c/fdb876c193e3888ff8cd0824eef66596f1e6c7d80bff9e9bd4537556edd7/mo_dots-10.688.26234-py3-none-any.whl --output /work/wheels/mo_dots-10.688.26234-py3-none-any.whl \
    && echo '72d5125c0b114b88cbcf6bcd3cf2afd035a14dac44bae06bbc73e0e7042dba59  /work/wheels/mo_dots-10.688.26234-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/85/d4/38726838be7785b5b59e96ef627baea2f40fa43bc31d5bea8862505f14c3/mo_future-7.687.26234-py3-none-any.whl --output /work/wheels/mo_future-7.687.26234-py3-none-any.whl \
    && echo '0dcc914da04ad4068b2d5b90e5c5d50ae25e4b92a62723b1f2840b1963f1dff3  /work/wheels/mo_future-7.687.26234-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/44/2a/257aa0d928d03943727b130abbce6f87517eb4c8cfd54df3a49d6b88c9e9/mo_imports-7.687.26234-py3-none-any.whl --output /work/wheels/mo_imports-7.687.26234-py3-none-any.whl \
    && echo '4aae6340e918d018d419a54bbe8f103ad4beb6e78dd7749f19950da72ba17be6  /work/wheels/mo_imports-7.687.26234-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/6f/ea/f3f7de9690f0f71e6be232dd90a58c28f06b7dc9280f786e886901489962/mo_parsing-9.3.26234-py3-none-any.whl --output /work/wheels/mo_parsing-9.3.26234-py3-none-any.whl \
    && echo '4566f6d5b0c95edf067b68f3ca8d387ab6d92a97be51630ea7c9256f8f607fbd  /work/wheels/mo_parsing-9.3.26234-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b4/a9/507755a026dea854098fa9c6f806a6dd6a5fb9c8b463312b391a469f4c16/mo_sql_parsing-11.699.26234-py3-none-any.whl --output /work/wheels/mo_sql_parsing-11.699.26234-py3-none-any.whl \
    && echo 'b6870253593670074e91a2656b5558983befb22f77cee15fd4b26ec4ad031220  /work/wheels/mo_sql_parsing-11.699.26234-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/fd/ad/d4caf4b253ffe74021cbbe5488ceb3e66863f3581b5bc509e90537d5fd1c/mo_sql_parsing-11.699.26234.tar.gz --output /work/mo-sql-parsing-sdist.tar.gz \
    && echo '34cae547af8c07ea33b07cc351aaacab44d8c54350351aca23ea23d9c86037f2  /work/mo-sql-parsing-sdist.tar.gz' | sha256sum --check \
    && tar -xzf /work/mo-sql-parsing-sdist.tar.gz --strip-components=1 -C /work/mo-sql-parsing-sdist \
    && unzip -q /work/wheels/mo_sql_parsing-11.699.26234-py3-none-any.whl -d /work/mo-sql-parsing-wheel \
    && diff -r /work/mo-sql-parsing-sdist/mo_sql_parsing /work/mo-sql-parsing-wheel/mo_sql_parsing \
    && cd /work/mo-sql-parsing-sdist \
    && printf '%s\n' \
       'a14ac329eaf36191b434b9bd049daa3cdf27db7e8aa8675ddd1720045c3160de  mo_sql_parsing/sql_parser.py' \
       '60222c28c1a7f6a92c7df98e5c5f4459e624e6e285e0b9b94467af5f6ab3343d  LICENSE' \
       | sha256sum --check \
    && grep -qx 'Mozilla Public License, version 2.0' LICENSE
# Atheris 3.0.0 has no aarch64 wheel; it is built from its pinned sdist against Debian's clang-14 libFuzzer (orjson/pydantic precedent).
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f8/58/5965955898e16bee17c8379eae12194993bf641c4629016991248b862069/atheris-3.0.0.tar.gz -o /work/atheris.tar.gz \
    && echo '1f0929c7bc3040f3fe4102e557718734190cf2d7718bbb8e3ce6d3eb56ef5bb3  /work/atheris.tar.gz' | sha256sum --check \
    && mkdir /work/atheris-source && tar -xzf /work/atheris.tar.gz -C /work/atheris-source --strip-components=1 \
    && python3 -m venv /opt/atheris-build \
    && printf '%s\n' 'wheel==0.48.0 --hash=sha256:3217dcc807155e45db462d7ef2431f5ddda0d7273b700d05a67b271ceb1287ab' 'packaging==26.3 --hash=sha256:d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c' 'pybind11==3.1.0 --hash=sha256:b8488090f8acffbcb6b5d6a85571a6827a0a2981ffb75e5a0b27b87c4a6b7dd0' | /opt/atheris-build/bin/pip install --no-deps --require-hashes -r /dev/stdin \
    && LIBFUZZER_LIB=/usr/lib/llvm-14/lib/clang/14.0.6/lib/linux/libclang_rt.fuzzer-aarch64.a \
       /opt/atheris-build/bin/pip wheel --no-build-isolation --no-deps /work/atheris-source -w /work/atheris-wheel
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && /opt/venv/bin/pip install --no-index --no-deps /work/atheris-wheel/atheris-*.whl \
    && /opt/venv/bin/pip check \
    && diff -r --exclude=__pycache__ /work/mo-sql-parsing-wheel/mo_sql_parsing /opt/venv/lib/python3.11/site-packages/mo_sql_parsing \
    && /opt/venv/bin/python -c 'from mo_sql_parsing import parse; print(parse("SELECT 1"))' \
    && { python3 --version; /opt/venv/bin/pip show mo-sql-parsing mo-parsing atheris | grep -E '^(Name|Version):'; cd /opt/venv/lib/python3.11/site-packages && sha256sum mo_sql_parsing/sql_parser.py mo_parsing/core.py; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py run-control.py /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
