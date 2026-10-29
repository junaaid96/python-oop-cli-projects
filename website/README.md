# Docs website

VitePress site published at https://junaaid96.github.io/python-oop-cli-projects/.

The repo Markdown is the single source: `scripts/sync.mjs` copies `README.md`, `docs/`, `docs/django/` and every `projects/NN_*/README.md` (plus the project's main modules) into a git-ignored `content/` folder at build time. `legacy/` is not published.

```bash
cd website
npm install
npm run dev      # http://localhost:5173/python-oop-cli-projects/
npm run build    # output in .vitepress/dist
```

Deployed by `.github/workflows/pages.yml` on every push to `main` that touches the docs.
