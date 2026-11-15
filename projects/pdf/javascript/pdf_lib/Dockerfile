FROM --platform=linux/arm64 node@sha256:af02d57b57719b9657a45199a79264a9437940cd55b3c7b3fc99615654f124a0 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund \
    && curl --fail --location --retry 3 https://registry.npmjs.org/pdf-lib/-/pdf-lib-1.17.1.tgz \
       --output /work/pdf-lib-1.17.1.tgz \
    && echo 'a7cc1eaf12e41e612a7be581162a63b18118aefc01e90f6a1f35347b1f324a1c  /work/pdf-lib-1.17.1.tgz' | sha256sum --check
RUN { node --version; npm --version; node -p 'require("pdf-lib/package.json").version'; \
       node -p 'require("@jazzer.js/core/package.json").version'; } > /work/toolchain.txt

FROM --platform=linux/arm64 node@sha256:af02d57b57719b9657a45199a79264a9437940cd55b3c7b3fc99615654f124a0
WORKDIR /work
COPY --from=build /work/node_modules /work/node_modules
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.js replay.js fuzz.js run-control.js /work/
ENTRYPOINT ["node", "/work/run-control.js"]
