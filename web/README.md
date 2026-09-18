# PhD Presentation — Liquid Glass (React)

A web presentation built with **React + Vite + TypeScript**, recreating all 13
slides of `../presentation/Delft Phd scrap handling - completed.pptx` with a
**Liquid Glass · white** design system (frosted glass sheets, drifting liquid
blobs, blue→indigo gradient accents).

## Run

```bash
cd web
npm install
npm run dev -- --host 0.0.0.0     # http://localhost:5173
npm run build                     # type-check + production bundle in dist/
```

## Controls

| Key / click            | Action                                        |
|------------------------|-----------------------------------------------|
| `←` `→` `space`        | previous / next slide                         |
| `Home` / `End`         | first / last slide                            |
| click progress bar     | jump to position                              |
| `G` / **▦ Overview**   | grid overview of all slides                   |
| `N` / **✎ Notes**      | speaker-notes drawer (verbatim PPTX script)   |
| `F` / **◇ Figma**      | Figma bridge panel                            |
| `⛶`                    | fullscreen                                    |

## Structure

- `src/slides.tsx` — the 13 slide components (1:1 content with the PPTX).
- `src/notes.ts` — speaker notes extracted verbatim from the PPTX.
- `src/theme.css` — the Liquid Glass white design system (glass primitives,
  liquid accents, tables, chrome).
- `src/App.tsx` — stage scaling (1280×720 design stage, fit-to-window),
  navigation, overview grid, notes drawer.
- `src/figma.ts` + `src/FigmaPanel.tsx` — client-side Figma REST API bridge.
- `public/img/` — images extracted from the PPTX (logos + 3 paper figures).

## Figma bridge

The **Figma** panel lets you load any Figma file from the browser and render
top-level nodes as PNG references — the same API surface a figma-to-react
pipeline uses:

- `GET /v1/files/:key?depth=2` → file name, pages, top-level nodes
- `GET /v1/images/:key?ids=…` → rendered node as PNG

Paste a Figma file URL (or key) + your personal access token, click **Load**,
then click a node to render it.

- The token is read from `VITE_FIGMA_TOKEN` in `web/.env.local`
  (gitignored — a template lives in `web/.env.example`), and can be overridden
  in the panel UI. The token is only ever sent to `api.figma.com`.
- Calls run **in the browser**, so they work from any machine with internet
  access to Figma.
