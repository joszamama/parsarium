FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/htmlparser2/-/htmlparser2-12.0.0.tgz --output /work/source.tgz \
    && echo 'bd21df686ef9b29b6786aac9aa75a9d20e1e884ad3f3089882db1d576dd4aaa0  /work/source.tgz' | sha256sum --check \
    && curl --fail --location --retry 3 https://registry.npmjs.org/entities/-/entities-8.1.0.tgz --output /work/entities.tgz \
    && echo 'e9a27d66db0d0a6f2d76454219d94f5729ae2a29f08ab06c92e5f6eaa37cbe68  /work/entities.tgz' | sha256sum --check
RUN { node --version; npm --version; npm ls htmlparser2 entities @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
