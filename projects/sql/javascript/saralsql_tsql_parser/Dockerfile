FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/@saralsql/tsql-parser/-/tsql-parser-0.4.7.tgz --output /work/source.tgz \
    && echo '939262514c4f61ad2e4476954706c43465aa5fd372acc493f2560aa5087b4f31  /work/source.tgz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tgz -C /work/source \
    && diff -r /work/source/package /work/node_modules/@saralsql/tsql-parser \
    && grep -q '"license": "MIT"' /work/node_modules/@saralsql/tsql-parser/package.json \
    && grep -q '^MIT License' /work/node_modules/@saralsql/tsql-parser/LICENSE
RUN { node --version; npm --version; npm ls @saralsql/tsql-parser @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.js harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
