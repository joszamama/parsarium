# Parsarium website

Parsarium is a static site generated from the repository's parser evidence and runnable target manifests. Its routes are real HTML pages: Home, Atlas, Run, Lab, and Why parsers. They work directly at the GitHub Pages project path and on refresh.

## Preview locally

From the repository root:

```sh
python3 website/build.py
python3 -m http.server 8765 --directory website/dist
```

Open `http://localhost:8765/`. `website/build.py` checks the 80 cell counts and guide links, writes one shared catalog JSON file, and copies one valid control for each format. The Atlas shows recorded within-cell adoption ranks and metrics. The Run page shows saved control evidence and commands for pinned Docker harnesses. The Lab executes small PNG, SVG, and ASCII PNM parsers in the browser, then separates those live results from saved Docker receipts. Its byte clues for all ten formats use offsets and output keys checked during the build.

## Publish on GitHub Pages

In the repository's **Settings → Pages**, choose **GitHub Actions** as the deployment source. The `Publish site` workflow deploys relevant changes on `main` and can run manually. The site has no server, database, or JavaScript build step.

The Atlas links to format and parser guides, rankings, evidence, and harness manifests in the main repository. A private repository's links require repository read access until it is made public. Counts are generated from the current audit during each build.
