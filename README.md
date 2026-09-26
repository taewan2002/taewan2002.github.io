# Taewan Cho — Academic Website

Personal academic website for https://taewan2002.github.io/.

The site is plain HTML and CSS. No build step or external dependencies are required.

## Edit

- `index.html`: biography, research interests, publications, and links.
- `styles.css`: typography, colors, spacing, and responsive layout.
- `assets/`: profile photo and publication thumbnails. Each thumbnail opens at full size.
- `ASSET-SOURCES.md`: sources for the original paper figures used in all seven publication thumbnails.
- `.nojekyll`: serves the static files directly on GitHub Pages.

## Preview

Open `index.html` in a browser, or serve this directory with a local HTTP server.

## Publish to GitHub Pages

1. Create the public repository `taewan2002/taewan2002.github.io`.
2. Add the files in this directory to the repository's `main` branch.
3. In **Settings → Pages**, choose **Deploy from a branch**.
4. Select **main** and **/ (root)**, then save.
5. Wait for the Pages deployment to finish and check https://taewan2002.github.io/.

See the [GitHub Pages quickstart](https://docs.github.com/en/pages/quickstart).

## Design

The image-led publication list takes inspiration from [Jon Barron's academic website](https://jonbarron.info/), with a responsive CSS grid implementation. This site does not depend on Jekyll. The brief biography foregrounds swarm robotics and multi-agent autonomous systems as research interests, and lists previous publications without recasting them as swarm robotics results.
