FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/dt-sql-parser/-/dt-sql-parser-4.6.1.tgz --output /work/source.tgz \
    && echo '0f989e624714580c4281d5bb4a4b45eaa31274546f24041c7278aff32e19299e  /work/source.tgz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tgz -C /work/source \
    && diff -r /work/source/package /work/node_modules/dt-sql-parser \
    && grep -q '"license": "MIT"' /work/node_modules/dt-sql-parser/package.json \
    && grep -q '^MIT License' /work/node_modules/dt-sql-parser/LICENSE
RUN { node --version; npm --version; npm ls dt-sql-parser antlr4ng antlr4-c3 @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.js harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
