FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/yaml.min/-/yaml.min-2.0.0.tgz --output /work/source.tgz \
    && echo '5f41337f6a4ee90925dbd2ea12464e994c50d7c93fa230336bf51ad89300b6f1  /work/source.tgz' | sha256sum --check \
    && mkdir /work/src && tar -xzf /work/source.tgz -C /work/src \
    && diff -r /work/src/package/lib /work/node_modules/yaml.min/lib \
    && cmp /work/src/package/LICENSE /work/node_modules/yaml.min/LICENSE
RUN { node --version; npm --version; npm ls yaml.min @jazzer.js/core --depth=0; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
