FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/yaml-eslint-parser/-/yaml-eslint-parser-2.1.0.tgz --output /work/source.tgz \
    && echo 'f6c2d73f9dbbc7239811a13bcb63ff9fdb36b6103d703c473d32f7ab2d4098e8  /work/source.tgz' | sha256sum --check \
    && mkdir /work/src && tar -xzf /work/source.tgz -C /work/src \
    && diff -r /work/src/package/lib /work/node_modules/yaml-eslint-parser/lib \
    && cmp /work/src/package/LICENSE /work/node_modules/yaml-eslint-parser/LICENSE \
    && curl --fail --location --retry 3 https://registry.npmjs.org/yaml/-/yaml-2.9.1.tgz --output /work/underlying.tgz \
    && echo '4ef6c54cf559b8a207b7b518378230805a1c84af239b14960e8c67c7d59de5d3  /work/underlying.tgz' | sha256sum --check \
    && mkdir /work/underlying && tar -xzf /work/underlying.tgz -C /work/underlying \
    && diff -r /work/underlying/package/dist /work/node_modules/yaml/dist \
    && cmp /work/underlying/package/LICENSE /work/node_modules/yaml/LICENSE
RUN { node --version; npm --version; npm ls yaml-eslint-parser yaml @jazzer.js/core --depth=0; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
