# Parsarium website

Parsarium is a static site at [parsarium.com](https://parsarium.com), generated from the repository's parser evidence and runnable target manifests. Its routes are real HTML pages: Home, Atlas, About, Run locally, and Learn. They work directly on refresh. The former `/why/` route points to About.

## Preview locally

From the repository root:

```sh
python3 website/build.py
python3 -m http.server 8765 --directory website/dist
```

Open `http://localhost:8765/`. `website/build.py` checks counts and guide links for every format and ecosystem, writes one shared catalog JSON file, and copies one valid control for each format. The Atlas shows adoption ranks among parsers that handle the same format in the same ecosystem. About explains the research motivation and evidence. Run locally teaches one-target replay and the `run-format` Docker batch. Learn is a short book about grammar and parser observations; its browser exercise reveals structure before the result. Its control-file questions cover all ten current formats and use saved parser observations checked during the build.

## Publish on GitHub Pages

In the repository's **Settings → Pages**, choose **GitHub Actions** as the deployment source and set the custom domain to `parsarium.com`. The `Publish site` workflow deploys relevant changes on `main` and can run manually. The build writes `CNAME` into the Pages artifact. The site has no server, database, or JavaScript build step.

The Atlas links to format and parser guides, rankings, evidence, and harness manifests in the main repository. A private repository's links require repository read access until it is made public. Counts are generated from the current audit during each build.

All main pages include the Cloudflare Web Analytics beacon for `parsarium.com`. The site remains hosted on GitHub Pages; analytics does not require moving DNS to Cloudflare.
