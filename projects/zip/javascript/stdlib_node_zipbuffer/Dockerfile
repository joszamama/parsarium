FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
WORKDIR /work
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
RUN echo '71b004f18a82f3ea8f26109798564a12e5e4c7989a4c35b93851830b5815dd03  /usr/local/bin/node' | sha256sum --check
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/@jazzer.js/core/-/core-4.0.0.tgz --output /work/jazzer-core.tgz \
    && echo '7f281856b36dde6fcd1b078c40c9f74b01ed1f61b9314cd882e0409651dc0431  /work/jazzer-core.tgz' | sha256sum --check
RUN { node --version; npm --version; npm ls @jazzer.js/core --depth=0; } > /work/toolchain.txt
FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
