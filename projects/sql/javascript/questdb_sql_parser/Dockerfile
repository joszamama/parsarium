FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/@questdb/sql-parser/-/sql-parser-0.1.22.tgz --output /work/source.tgz \
    && echo '6d2626fc7ceedbc87a8a1d222a6d46aa9f2581b077309959daf8bb3e45e07aaf  /work/source.tgz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tgz -C /work/source \
    && diff -r /work/source/package /work/node_modules/@questdb/sql-parser \
    && grep -q '"license": "Apache-2.0"' /work/node_modules/@questdb/sql-parser/package.json \
    && grep -q 'Apache License' /work/node_modules/@questdb/sql-parser/LICENSE
RUN { node --version; npm --version; npm ls @questdb/sql-parser chevrotain @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.js harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
