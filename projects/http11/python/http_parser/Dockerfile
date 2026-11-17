FROM --platform=linux/amd64 python@sha256:e428f090ae6d8bb371deaa3216a023c4828f85a0334a468f09fdc9254e527988 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-14-dev llvm make \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://files.pythonhosted.org/packages/04/b2/c98d0a2b759fcf91ae0a3e7691e840e4c861dac2c7f5a4e36220129d0cc8/http-parser-0.9.0.tar.gz \
    -o /work/http-parser-0.9.0.tar.gz \
    && echo '441d3a57c6227230f98aa97539da006fda0f8f4880bc4c5cd895ff2138a52621  /work/http-parser-0.9.0.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/http-parser-0.9.0.tar.gz -C /work/source --strip-components=1 \
    && echo '82f66abb9da6c79843189e3e10153d255f2dde120f78c557205de0f3a840bfc2  /work/source/http_parser/http_parser.c' | sha256sum --check \
    && echo '587c3a477d80c3354bf13c090652a63ff39d0cd52e76a2240acd2d7e0e1866bf  /work/source/http_parser/parser.c' | sha256sum --check \
    && curl --fail --location --retry 3 \
    https://files.pythonhosted.org/packages/50/db/d141a3ac3974d267946b49abaeedea999725eca44a34534b8c5450356e8f/atheris-2.3.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    -o /work/atheris-2.3.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl \
    && echo 'b91cb296d60915c3efa4f6db48f09c4678b574cddb7ca98035f1cb9d9fb96f64  /work/atheris-2.3.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl' | sha256sum --check
COPY build.sh /work/build.sh
RUN chmod +x /work/build.sh && /work/build.sh \
    && { /opt/venv/bin/python --version; clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/amd64 python@sha256:e428f090ae6d8bb371deaa3216a023c4828f85a0334a468f09fdc9254e527988
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py run-control.py run-control.sh /work/
ENV LLVM_PROFILE_FILE=/dev/null
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
