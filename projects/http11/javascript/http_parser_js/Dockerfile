FROM --platform=linux/arm64 node@sha256:af02d57b57719b9657a45199a79264a9437940cd55b3c7b3fc99615654f124a0 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/http-parser-js/-/http-parser-js-0.5.10.tgz \
       --output /work/http-parser-js-0.5.10.tgz \
    && echo 'ab1672c31c6392825adaf4b61796a979beeea0daaffb10484f0da20238fd94e4  /work/http-parser-js-0.5.10.tgz' | sha256sum --check
RUN { node --version; npm --version; node -p 'require("http-parser-js/package.json").version'; \
       node -p 'require("@jazzer.js/core/package.json").version'; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:af02d57b57719b9657a45199a79264a9437940cd55b3c7b3fc99615654f124a0
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
