FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/@xml-tools/parser/-/parser-1.0.12.tgz --output /work/source.tgz \
    && echo 'cd301c11544f5f4da0272f6d3623ea39cfa68c85efe92e696d6d0be0fe629a84  /work/source.tgz' | sha256sum --check \
    && curl --fail --location --retry 3 https://registry.npmjs.org/chevrotain/-/chevrotain-7.1.1.tgz --output /work/chevrotain.tgz \
    && echo '9cbea943f1aef15a1054d3e3d8f0cfb3736720ae77a926df9a83207f6bf522af  /work/chevrotain.tgz' | sha256sum --check
RUN { node --version; npm --version; npm ls @xml-tools/parser chevrotain @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.js harness.js replay.js fuzz.js run-control.js manifest.json /work/
ENTRYPOINT ["node", "/work/run-control.js"]
