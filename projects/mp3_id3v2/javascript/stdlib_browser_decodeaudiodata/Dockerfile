FROM --platform=linux/arm64 mcr.microsoft.com/playwright@sha256:a0f4498920a5dbac63196d9140ed738ef00470f27e2e74029abd8850b7bd5717
WORKDIR /work
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
RUN echo 'f5d89353cc9ef8dc1541268bbee1f05ee40a31ce3d9799b3a274e5147f6a8cdb  /ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux-arm64/chrome-headless-shell' | sha256sum --check
COPY package.json package-lock.json ./
RUN npm ci --omit=dev --ignore-scripts --no-audit --no-fund
COPY browser-harness.js replay.mjs run-control.mjs ./
ENTRYPOINT ["node", "/work/run-control.mjs"]
