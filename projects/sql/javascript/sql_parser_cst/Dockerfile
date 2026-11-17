FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/sql-parser-cst/-/sql-parser-cst-0.44.1.tgz --output /work/source.tgz \
    && echo '1dc65d972c20779a9beb6aafbc72bad16575bca83b8e09acf33aa12e7549b2af  /work/source.tgz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tgz -C /work/source \
    && diff -r /work/source/package /work/node_modules/sql-parser-cst \
    && grep -q '"license": "GPL-2.0-or-later"' /work/node_modules/sql-parser-cst/package.json \
    && grep -q 'GNU GENERAL PUBLIC LICENSE' /work/node_modules/sql-parser-cst/LICENSE
RUN { node --version; npm --version; npm ls sql-parser-cst @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.js harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
