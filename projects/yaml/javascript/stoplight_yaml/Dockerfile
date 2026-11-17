FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/@stoplight/yaml/-/yaml-4.3.0.tgz --output /work/source.tgz \
    && echo '3946780548738b9f1f0a03fda669a7208b0bcf271647330ae89ae143532e9943  /work/source.tgz' | sha256sum --check \
    && mkdir /work/src && tar -xzf /work/source.tgz -C /work/src \
    && diff -r -x node_modules /work/src/package /work/node_modules/@stoplight/yaml \
    && curl --fail --location --retry 3 https://registry.npmjs.org/@stoplight/yaml-ast-parser/-/yaml-ast-parser-0.0.50.tgz --output /work/underlying.tgz \
    && echo 'aaabcb6ac5e0e0fbd17a14fbd81f32cacf4b0cb0644c5e8359a1c358bde0fc68  /work/underlying.tgz' | sha256sum --check \
    && mkdir /work/underlying && tar -xzf /work/underlying.tgz -C /work/underlying \
    && diff -r /work/underlying/package/dist/src /work/node_modules/@stoplight/yaml-ast-parser/dist/src \
    && cmp /work/underlying/package/license.txt /work/node_modules/@stoplight/yaml-ast-parser/license.txt
RUN { node --version; npm --version; npm ls @stoplight/yaml @stoplight/yaml-ast-parser @jazzer.js/core --depth=0; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
