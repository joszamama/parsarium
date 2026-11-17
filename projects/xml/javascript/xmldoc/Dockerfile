FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/xmldoc/-/xmldoc-3.0.0.tgz --output /work/source.tgz \
    && echo '5546bf0c619adf2b7583797849d905b5e0e92ef3cfcf2b5f04bc0ca49d570e2a  /work/source.tgz' | sha256sum --check \
    && curl --fail --location --retry 3 https://registry.npmjs.org/sax/-/sax-1.6.1.tgz --output /work/sax.tgz \
    && echo '6e9abf03478608b80894bb8b6421271a0e583504f785f749a700d6bb35be85bd  /work/sax.tgz' | sha256sum --check \
    && mkdir /work/release && tar -xzf /work/source.tgz -C /work/release \
    && cmp /work/release/package/dist/index.js /work/node_modules/xmldoc/dist/index.js \
    && cmp /work/release/package/LICENSE /work/node_modules/xmldoc/LICENSE
RUN { node --version; npm --version; npm ls xmldoc sax @jazzer.js/core --depth=1; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY adapter.mjs harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
