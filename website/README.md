# Parsarium website

The website is generated from the repository's parser evidence and runnable target manifests. It runs at a GitHub Pages project URL, including the `/parsarium/` path. No server, database, or JavaScript build tool is required.

## Preview locally

From the repository root:

```sh
python3 website/build.py
python3 -m http.server 8765 --directory website/dist
```

Open `http://localhost:8765/`. The build checks the catalog's 80 cell counts and copies the six displayed valid controls. The control viewer replays saved manifest results; it does not execute parser code in the browser.

## Publish on GitHub Pages

In the repository's **Settings → Pages**, choose **GitHub Actions** as the build and deployment source. The `Publish field guide` workflow deploys changes to the website, catalog, projects, or controls on `main`. It can also run manually from the Actions tab. No repository secrets are needed.

The repository is currently private. GitHub Pages needs a plan that supports private repositories, and a Pages site is public by default. The site's GitHub links to evidence and harness source require repository read access until the repository is made public.

The atlas links to rankings, evidence, and harness manifests in the main repository. The site preserves the distinction between 1,636 verified third-party package paths, 45 recorded standard/runtime APIs, and 83 runnable project harnesses.
