FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/JSONStream/-/JSONStream-1.3.5.tgz --output /work/source.tgz \
    && echo 'ef3be72c45c76fbb688e2cb3078a7905b413ec9c8eb2d889cd0481f38c712488  /work/source.tgz' | sha256sum --check \
    && curl --fail --location --retry 3 https://registry.npmjs.org/jsonparse/-/jsonparse-1.3.1.tgz --output /work/underlying.tgz \
    && echo 'cf6c2edd3a8f77080beabb6c46b51e5853b61422341a0ef2e05a9e83a90bffce  /work/underlying.tgz' | sha256sum --check \
    && curl --fail --location --retry 3 https://registry.npmjs.org/through/-/through-2.3.8.tgz --output /work/through.tgz \
    && echo '16b27a8c0fb13e5727356b328d72dbbc5f20bd909252f14d19da344e9354573e  /work/through.tgz' | sha256sum --check
RUN { node --version; npm --version; npm ls JSONStream jsonparse through @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
