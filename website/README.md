# Parsarium website

Parsarium is a static site at [parsarium.com](https://parsarium.com), generated from the repository's parser evidence and runnable target manifests. Its routes are real HTML pages: Home, About, Atlas, Run locally, and Learn. Each has a Spanish counterpart under `/es/`. Pages work directly on refresh, and the EN/ES switch preserves the current query and hash. The former `/why/` route points to About.

## Preview locally

From the repository root:

```sh
python3 website/build.py
python3 -m http.server 8765 --directory website/dist
```

Open `http://localhost:8765/` or `http://localhost:8765/es/`. `website/build.py` checks counts and guide links for every format and ecosystem, writes one shared catalog JSON file, copies one valid control for each format, and generates the bilingual sitemap and canonical links. The Atlas shows adoption ranks among parsers that handle the same format in the same ecosystem. About explains the research motivation and evidence. Run locally teaches one-target replay and the `run-format` Docker batch. Learn is a short book about grammar and parser observations; its browser exercise reveals structure before the result. Its control-file questions cover all ten current formats and use saved parser observations checked during the build. The Spanish site translates the interface and lessons; API names, commands, metrics, and source evidence retain their original wording from the repository.

The visual language uses softened slate and mint surfaces, compact monospaced labels for file structure, and a three-part input → API → observation example on Home. The Learn terminal remains small enough to keep the structure and result panels visible alongside it on a wide screen.

## Publish on GitHub Pages

In the repository's **Settings → Pages**, choose **GitHub Actions** as the deployment source and set the custom domain to `parsarium.com`. The `Publish site` workflow deploys relevant changes on `main` and can run manually. The build writes `CNAME` into the Pages artifact. The site has no server, database, or JavaScript build step.

The Atlas links to format and parser guides, rankings, evidence, and harness manifests in the main repository. A private repository's links require repository read access until it is made public. Counts are generated from the current audit during each build.

All English and Spanish pages include the Cloudflare Web Analytics beacon for `parsarium.com`. The site remains hosted on GitHub Pages; analytics does not require moving DNS to Cloudflare.
