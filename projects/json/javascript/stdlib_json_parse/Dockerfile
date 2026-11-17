FROM --platform=linux/arm64 node@sha256:c8890e48c4572d2f912bf787272b34d122a4009911a5aafe604912194ff89c47
RUN echo '71b004f18a82f3ea8f26109798564a12e5e4c7989a4c35b93851830b5815dd03  /usr/local/bin/node' | sha256sum --check
WORKDIR /work
COPY adapter.mjs second-control.json run-control.js /work/
RUN echo 'e8e24e794840f27e21c13e9f7266c4803cf5976f9da2674fc6552d671d2c44e2  /work/adapter.mjs' | sha256sum --check \
    && echo 'a54ab095e6fd9281696c461d7385b759b99129ccd14d5242de084e5868dc7762  /work/second-control.json' | sha256sum --check \
    && { node --version; node -p '"v8 " + process.versions.v8'; } > /work/toolchain.txt
ENTRYPOINT ["node", "/work/run-control.js"]
