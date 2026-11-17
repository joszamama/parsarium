FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/lossless-json/-/lossless-json-4.3.3.tgz --output /work/source.tgz \
    && echo '89652330e5ef627ada0d428c509a257f775a0685e5a7019714b6a4be943d032c  /work/source.tgz' | sha256sum --check
RUN { node --version; npm --version; npm ls lossless-json @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js fuzz.js run-control.js manifest.json /work/
ENTRYPOINT ["node", "/work/run-control.js"]
