# Personal

## bot-crossing

[bot-crossing](https://github.com/jarrenrocks/bot-crossing) is included as a git
submodule in [`bot-crossing/`](./bot-crossing). It's a local, browser-based tool
that visualizes your AI coding-agent sessions as a colony of astronauts on an
explorable 3D planet (Three.js + a small Node API), running entirely on
`127.0.0.1` with no accounts or cloud uploads.

### Getting the submodule

If you cloned this repo without `--recurse-submodules`, pull the submodule
contents:

```bash
git submodule update --init --recursive
```

### Running it

```bash
cd bot-crossing
npm install
npm run dev
```

`npm run dev` starts both the API and the Vite dev server. See
[`bot-crossing/README.md`](./bot-crossing/README.md) for production mode,
graphics presets, and configuration.

### Updating to the latest upstream version

```bash
cd bot-crossing
git pull origin main
cd ..
git add bot-crossing
git commit -m "Update bot-crossing submodule"
```
