FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/@noelminamino/dns-packet/-/dns-packet-7.1.1.tgz --output /work/source.tgz \
    && echo '7409d7a4ef382d1bd3b3ac144b077e179252891a2d4658c9bbc113b596b929f6  /work/source.tgz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tgz -C /work/source \
    && diff -r --exclude=node_modules /work/source/package /work/node_modules/@noelminamino/dns-packet \
    && grep -q '"license": "MIT"' /work/node_modules/@noelminamino/dns-packet/package.json
RUN { node --version; npm --version; npm ls @noelminamino/dns-packet @leichtgewicht/ip-codec utf8-codec @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
