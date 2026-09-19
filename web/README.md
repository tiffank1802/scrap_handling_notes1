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
- `src/figma.ts` — client-side Figma REST client (`GET /v1/files`, `GET /v1/images`).
- `src/figmaToReact.ts` — Figma node-tree → React styles + JSX serializer.
- `src/FigmaRenderer.tsx` — live renderer: draws a Figma node tree as React/CSS.
- `src/FigmaPanel.tsx` — the in-app Figma → React bridge (F key).
- `scripts/figma-to-react.mjs` — Node generator (uses the `figma-api` package).
- `scripts/sample-slide.json` — sample Figma file model (REST response shape).
- `src/figma/generated/` — committed code generated from the sample (proof).
- `public/img/` — images extracted from the PPTX (logos + 3 paper figures).

## Figma → React pipeline (components → code)

This deck is generated **from Figma data**, not hand-drawn: the Figma REST
API node tree (the same model a design-to-code tool consumes) is walked and
emitted as React components with inline styles.

### Node generator (uses the `figma-api` package)

```bash
# from a real Figma file (token from web/.env.local or FIGMA_TOKEN env)
npm run figma:generate -- --file <fileKey>            # all top-level frames
npm run figma:generate -- --file <fileKey> --node <id>

# offline / reproducible (this is what produced the committed output)
npm run figma:generate -- --from-json scripts/sample-slide.json
```

Output → `src/figma/generated/slides.generated.tsx` (one component per slide
frame). `scripts/sample-slide.json` is a Figma file model in the exact
`GET /v1/files/:key` response shape; run it to reproduce the committed code.

### Browser bridge (in-app)

Press **F / ◇ Figma** in the deck:

- **▶ Load bundled sample** — renders `scripts/sample-slide.json` live
- paste a **Figma file URL** + token → `GET /v1/files/:key`
- **live render**: the node tree drawn as React/CSS (`FigmaRenderer.tsx`)
- **Copy React code / Download .tsx**: `figmaTreeToReact` serializes the
  tree to JSX (the same code the Node generator writes)
- **PNG mode**: `GET /v1/images/:key?ids=…` per top-level node

### Mapping (Figma → CSS/React)

| Figma | React / CSS |
|---|---|
| `absoluteBoundingBox` | `position: absolute; left/top/width/height` (relative to parent) |
| `layoutMode` + `itemSpacing` + paddings + axis alignment | `display: flex` + `gap`/`padding`/`justify-content`/`align-items` |
| `fills` SOLID | `background: rgb()/rgba()` (TEXT fills → `color`) |
| `fills` GRADIENT_LINEAR | `linear-gradient(angle, stops…)` from gradient handles |
| `strokes` + `strokeWeight` | `border` |
| `cornerRadius` / `rectangleCornerRadii` | `border-radius` (incl. 4-corner) |
| `effects` DROP_SHADOW | `box-shadow` |
| `effects` BACKGROUND_BLUR | `backdrop-filter: blur(…)` (the glass!) |
| `TEXT.style` (family, weight, size, tracking, leading, align) | font CSS + `color` |
| `VECTOR` / `BOOLEAN_OPERATION` | labelled placeholder — export via `GET /v1/images/:key` |

The mapping lives in `src/figmaToReact.ts` (browser) and is mirrored in
`scripts/figma-to-react.mjs` (Node) — keep them in sync. The same walk would
run unchanged inside a **Figma native plugin** (`@figma/plugin-typings`) if
you prefer in-editor code generation.

### Token

- Read from `VITE_FIGMA_TOKEN` in `web/.env.local` (gitignored — template in
  `web/.env.example`), or set in the panel UI. The token is only ever sent to
  `api.figma.com`. Browser calls run in your browser (this dev sandbox's
  egress blocks `api.figma.com`, which is exactly why the pipeline also
  supports `--from-json`).
