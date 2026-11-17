FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/@visulima/yaml/-/yaml-2.0.0.tgz --output /work/source.tgz \
    && echo '54ab430434c522210b4ed4045e4a42c8cebda9abc53023ae631c7b9c25a6d12c  /work/source.tgz' | sha256sum --check \
    && mkdir /work/src && tar -xzf /work/source.tgz -C /work/src \
    && diff -r /work/src/package/dist /work/node_modules/@visulima/yaml/dist \
    && cmp /work/src/package/LICENSE.md /work/node_modules/@visulima/yaml/LICENSE.md
RUN { node --version; npm --version; npm ls @visulima/yaml @jazzer.js/core --depth=0; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
