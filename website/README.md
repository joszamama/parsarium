# Parsarium website

The website is generated from the repository's parser evidence and runnable target manifests. It runs at a GitHub Pages project URL, including the `/parsarium/` path. No server, database, or JavaScript build tool is required.

## Preview locally

From the repository root:

```sh
python3 website/build.py
python3 -m http.server 8765 --directory website/dist
```

Open `http://localhost:8765/`. The build checks the catalog's 80 cell counts and parser guide links, embeds the catalog in the built page, and copies one valid control for each of the ten formats. The format wall filters the atlas and updates the example. Atlas cards show recorded within-cell adoption ranks and metrics, leaving unknown values unranked. Every runnable card opens target-specific commands and saved control evidence in the workbench. The receipt walkthrough follows the selected target through control input, parser API, observed result, and corpus replay. The website does not execute parsers in the browser.

## Publish on GitHub Pages

In the repository's **Settings → Pages**, choose **GitHub Actions** as the build and deployment source. The `Publish site` workflow deploys changes to the website, catalog, projects, or controls on `main`. It can also run manually from the Actions tab. No repository secrets are needed.

The repository is currently private. GitHub Pages needs a plan that supports private repositories, and a Pages site is public by default. The site's GitHub links to evidence and harness source require repository read access until the repository is made public.

The atlas links to format and parser guides, rankings, evidence, and harness manifests in the main repository. The site preserves the distinction between verified third-party package paths, recorded standard/runtime APIs, and runnable project harnesses. Counts are generated from the current audit when the site is built.
