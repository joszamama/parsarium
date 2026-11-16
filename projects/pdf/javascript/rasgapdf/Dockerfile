FROM --platform=linux/amd64 node@sha256:af02d57b57719b9657a45199a79264a9437940cd55b3c7b3fc99615654f124a0 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/rasgapdf/-/rasgapdf-0.4.2.tgz --output /work/source.tgz \
    && echo 'da233b38df413bb15f4d866aa84c31eaa8f679ef1c2722de1a8899822b900843  /work/source.tgz' | sha256sum --check
RUN { node --version; npm --version; npm ls rasgapdf @jazzer.js/core --depth=0; } > /work/toolchain.txt

FROM --platform=linux/amd64 node@sha256:af02d57b57719b9657a45199a79264a9437940cd55b3c7b3fc99615654f124a0
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
