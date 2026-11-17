FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/jsdom/-/jsdom-31.0.1.tgz --output /work/source.tgz \
    && echo '53b0b47dbcebe37833e4cbcf162d9fc628a038eeddcb1e68255a4957381da109  /work/source.tgz' | sha256sum --check \
    && curl --fail --location --retry 3 https://registry.npmjs.org/saxes/-/saxes-6.0.0.tgz --output /work/saxes.tgz \
    && echo '1cdf52fbbe1ccbd175c365d2b8e63f46e590e74aff23fa6a44a6ec51522e96db  /work/saxes.tgz' | sha256sum --check
RUN { node --version; npm --version; npm ls jsdom saxes xmlchars @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js construct.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
