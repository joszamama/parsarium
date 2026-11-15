# Parsarium website

The website is generated from the repository's parser evidence and runnable target manifests. It runs at a GitHub Pages project URL, including the `/parsarium/` path. No server, database, or JavaScript build tool is required.

## Preview locally

From the repository root:

```sh
python3 website/build.py
python3 -m http.server 8765 --directory website/dist
```

Open `http://localhost:8765/`. The build checks the catalog's 80 cell counts and all parser guide links, embeds the catalog in the built page so the interface has no separate data request, and copies one valid control for each of the ten formats. Section 03 shows saved manifest results and commands for running a file, replaying a corpus, and preparing AFL++. Section 04 follows that file through generation, parsing, verification, and replay. Its parser result and covered-line count come from committed control receipts. The website does not execute parsers in the browser.

## Publish on GitHub Pages

In the repository's **Settings → Pages**, choose **GitHub Actions** as the build and deployment source. The `Publish site` workflow deploys changes to the website, catalog, projects, or controls on `main`. It can also run manually from the Actions tab. No repository secrets are needed.

The repository is currently private. GitHub Pages needs a plan that supports private repositories, and a Pages site is public by default. The site's GitHub links to evidence and harness source require repository read access until the repository is made public.

The atlas links to format and parser guides, rankings, evidence, and harness manifests in the main repository. The site preserves the distinction between 1,636 verified third-party package paths, 45 recorded standard/runtime APIs, and 109 runnable project harnesses.
