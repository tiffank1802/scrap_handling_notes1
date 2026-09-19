#!/usr/bin/env node
/* ============================================================
   figma-to-react — Figma → React code generator (Node)
   ----------------------------------------------------------
   Uses the `figma-api` package (typed wrapper of Figma's
   official REST API spec) to pull a file's node tree and emit
   React components (inline styles) into
   src/figma/generated/slides.generated.tsx.

   Usage:
     node scripts/figma-to-react.mjs --file <fileKey> [--node <nodeId>]
     node scripts/figma-to-react.mjs --from-json scripts/sample-slide.json

   Token: FIGMA_TOKEN env var, or VITE_FIGMA_TOKEN in web/.env.local
   (the same token the browser panel uses).

   NOTE: this script mirrors the mapping in src/figmaToReact.ts —
   keep the two in sync. The same walk would also run inside a
   Figma native plugin (@figma/plugin-typings) if you prefer
   in-editor code generation.
   ============================================================ */

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

// ---------- arg parsing ----------
const args = process.argv.slice(2);
const get = (flag) => {
  const i = args.indexOf(flag);
  return i >= 0 ? args[i + 1] : undefined;
};
const fileKey = get("--file");
const nodeId = get("--node");
const fromJson = get("--from-json");
const outArg = get("--out");
if (!fileKey && !fromJson) {
  console.error(
    "Usage:\n  node scripts/figma-to-react.mjs --file <fileKey> [--node <id>]\n  node scripts/figma-to-react.mjs --from-json <path>"
  );
  process.exit(1);
}

// ---------- token ----------
function loadToken() {
  if (process.env.FIGMA_TOKEN) return process.env.FIGMA_TOKEN;
  try {
    const envLocal = readFileSync(join(__dirname, "..", ".env.local"), "utf8");
    const m = envLocal.match(/^VITE_FIGMA_TOKEN=(.+)$/m);
    if (m) return m[1].trim();
  } catch {
    /* no .env.local */
  }
  return "";
}

// ---------- fetch ----------
let source;
if (fromJson) {
  source = JSON.parse(readFileSync(fromJson, "utf8"));
  console.log(`Loaded Figma file model from ${fromJson}`);
} else {
  const token = loadToken();
  if (!token) {
    console.error("No token: set FIGMA_TOKEN or add VITE_FIGMA_TOKEN to web/.env.local");
    process.exit(1);
  }
  const { Api } = await import("figma-api");
  const api = new Api({ personalAccessToken: token });
  console.log(`Fetching file ${fileKey} via Figma REST API (figma-api)…`);
  if (nodeId) {
    const res = await api.nodes.get({ fileKey, node_id: nodeId.replace(/:/g, "-") });
    source = res.nodes[Object.keys(res.nodes)[0]]?.document ?? res;
  } else {
    source = await api.files.get({ fileKey });
  }
}

// ---------- mapping (mirror of src/figmaToReact.ts) ----------
const cssColor = (c) => {
  const r = Math.round(c.r * 255), g = Math.round(c.g * 255), b = Math.round(c.b * 255);
  const a = c.a ?? 1;
  return a >= 1 ? `rgb(${r}, ${g}, ${b})` : `rgba(${r}, ${g}, ${b}, ${a})`;
};
function gradientToCss(fill) {
  const stops = (fill.gradientStops ?? [])
    .map((s) => `${cssColor(s.color)} ${(s.position * 100).toFixed(1)}%`)
    .join(", ");
  let angle = 90;
  const h = fill.gradientHandlePositions;
  if (h && h[0] && h[1]) angle = (Math.atan2(h[1].y - h[0].y, h[1].x - h[0].x) * 180) / Math.PI + 90;
  return `linear-gradient(${angle.toFixed(1)}deg, ${stops})`;
}
function fillsToBackground(fills) {
  if (!fills?.length) return undefined;
  const layers = [];
  for (const f of fills) {
    if (f.visible === false) continue;
    if (f.type === "SOLID" && f.color) layers.unshift(cssColor(f.color));
    else if (f.type === "GRADIENT_LINEAR" || f.type === "GRADIENT_RADIAL") layers.unshift(gradientToCss(f));
  }
  return layers.length ? layers.join(", ") : undefined;
}
function effectsToCss(node) {
  const out = {};
  const shadows = [];
  for (const e of node.effects ?? []) {
    if (e.visible === false) continue;
    if (e.type === "DROP_SHADOW" && e.color)
      shadows.push(`${e.offset?.x ?? 0}px ${e.offset?.y ?? 0}px ${e.radius ?? 0}px ${e.spread ?? 0}px ${cssColor(e.color)}`);
    else if (e.type === "BACKGROUND_BLUR") {
      out.backdropFilter = `blur(${e.radius ?? 0}px)`;
      out.WebkitBackdropFilter = `blur(${e.radius ?? 0}px)`;
    } else if (e.type === "LAYER_BLUR") out.filter = `blur(${e.radius ?? 0}px)`;
  }
  if (shadows.length) out.boxShadow = shadows.join(", ");
  return out;
}
const ALIGN = { MIN: "flex-start", CENTER: "center", MAX: "flex-end", SPACE_BETWEEN: "space-between" };
function figmaNodeToStyle(node, parent) {
  const style = {};
  const bb = node.absoluteBoundingBox;
  if (node.opacity !== undefined && node.opacity !== 1) style.opacity = node.opacity;
  const autoLayout = node.layoutMode === "HORIZONTAL" || node.layoutMode === "VERTICAL";
  if (autoLayout) {
    style.display = "flex";
    style.flexDirection = node.layoutMode === "HORIZONTAL" ? "row" : "column";
    if (node.itemSpacing !== undefined) style.gap = node.itemSpacing;
    const p = [node.paddingTop, node.paddingRight, node.paddingBottom, node.paddingLeft].filter((v) => v !== undefined);
    if (p.length) style.padding = p.join(" ");
    if (node.primaryAxisAlignItems) style.justifyContent = ALIGN[node.primaryAxisAlignItems];
    if (node.counterAxisAlignItems) style.alignItems = ALIGN[node.counterAxisAlignItems];
    if (node.layoutWrap === "WRAP") style.flexWrap = "wrap";
  } else if (bb) {
    const px = parent?.absoluteBoundingBox?.x ?? bb.x;
    const py = parent?.absoluteBoundingBox?.y ?? bb.y;
    style.position = "absolute";
    style.left = bb.x - px;
    style.top = bb.y - py;
    style.width = bb.width;
    style.height = bb.height;
  }
  const bg = fillsToBackground(node.fills);
  if (bg && node.type !== "TEXT") style.background = bg; // TEXT fills = text colour, not background
  if (node.strokes?.length && node.strokes[0]?.visible !== false && node.strokes[0]?.color)
    style.border = `${node.strokeWeight ?? 1}px solid ${cssColor(node.strokes[0].color)}`;
  if (node.cornerRadius !== undefined) style.borderRadius = node.cornerRadius;
  else if (node.rectangleCornerRadii?.length === 4) {
    const [tl, tr, br, bl] = node.rectangleCornerRadii;
    style.borderRadius = `${tl}px ${tr}px ${br}px ${bl}px`;
  }
  if (node.clipsContent) style.overflow = "hidden";
  Object.assign(style, effectsToCss(node));
  if (node.type === "ELLIPSE") style.borderRadius = "50%";
  if (node.type === "TEXT" && node.style) {
    style.fontFamily = `'${node.style.fontFamily ?? "Inter"}', sans-serif`;
    style.fontSize = node.style.fontSize ?? 14;
    style.fontWeight = node.style.fontWeight ?? 400;
    if (node.style.letterSpacing !== undefined) style.letterSpacing = node.style.letterSpacing;
    if (node.style.lineHeightPx !== undefined) style.lineHeight = node.style.lineHeightPx;
    const ta = node.style.textAlignHorizontal;
    if (ta) style.textAlign = ta === "CENTER" ? "center" : ta === "RIGHT" ? "right" : "left";
    const color = (node.fills ?? []).find((f) => f.type === "SOLID" && f.color);
    if (color) style.color = cssColor(color.color);
  }
  if (node.type === "LINE") {
    style.height = style.height ?? 1;
    if (!style.background) style.background = cssColor(node.strokes?.[0]?.color ?? { r: 0, g: 0, b: 0 });
  }
  return style;
}
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const styleLiteral = (style) => {
  const entries = Object.entries(style)
    .map(([k, v]) => `${/^[A-Za-z_$][A-Za-z0-9_$]*$/.test(k) ? k : JSON.stringify(k)}: ${typeof v === "string" ? JSON.stringify(v) : v}`)
    .join(", ");
  return `{${entries}}`;
};
function figmaTreeToJsx(node, indent = 0, parent) {
  if (node.visible === false) return `/* hidden node ${node.name} */\n`;
  const pad = "  ".repeat(indent);
  const attrs = `data-node="${node.id}" data-name="${esc(node.name)}"`;
  if (node.type === "TEXT") {
    const style = figmaNodeToStyle(node, parent);
    const text = esc(node.characters ?? "");
    return `${pad}<p ${attrs} style={${styleLiteral(style)}}>${text}</p>\n`;
  }
  const style = figmaNodeToStyle(node, parent);
  const children = (node.children ?? []).filter((c) => c.visible !== false);
  if (!children.length) {
    const isVector = node.type === "VECTOR" || node.type === "BOOLEAN_OPERATION";
    return `${pad}<div ${attrs} style={${styleLiteral(style)}}${isVector ? ` title="${esc(node.name)} — export via GET /v1/images/:key"` : ""} />\n`;
  }
  const inner = children.map((c) => figmaTreeToJsx(c, indent + 1, node)).join("");
  return `${pad}<div ${attrs} style={${styleLiteral(style)}}>\n${inner}${pad}</div>\n`;
}
const findSlideFrames = (document) => {
  const frames = [];
  for (const page of document?.children ?? [])
    if (page.type === "PAGE") for (const c of page.children ?? []) if (c.type === "FRAME" || c.type === "INSTANCE") frames.push(c);
  return frames.length ? frames : (document?.children ?? []).filter((c) => c.type === "FRAME");
};

// ---------- generate ----------
const doc = source.document ?? source;
const frames = findSlideFrames(doc);
if (!frames.length) {
  console.error("No top-level frames found in the Figma file model.");
  process.exit(1);
}

const slug = (s) => s.replace(/[^a-zA-Z0-9]+/g, "_").replace(/^_+|_+$/g, "").slice(0, 40) || "Slide";
let out = `// GENERATED by scripts/figma-to-react.mjs from "${source.name ?? fileKey ?? "Figma file"}"
// Do not edit by hand — re-run the generator to update.
// Node model → React mapping: src/figmaToReact.ts (kept in sync).
\n`;
const exportNames = [];
frames.forEach((frame, i) => {
  const name = `FigmaSlide_${i + 1}_${slug(frame.name)}`;
  exportNames.push(name);
  const body = figmaTreeToJsx(frame, 1);
  out += `export function ${name}() {\n  return (\n${body}  );\n}\n\n`;
});
out += `export const GENERATED_SLIDES = [\n${exportNames
  .map((n, i) => `  { name: ${JSON.stringify(frames[i].name)}, id: ${JSON.stringify(frames[i].id)}, component: ${n} },`)
  .join("\n")}\n];\n`;

const outPath = outArg ?? join(__dirname, "..", "src", "figma", "generated", "slides.generated.tsx");
mkdirSync(dirname(outPath), { recursive: true });
writeFileSync(outPath, out);
console.log(`Wrote ${frames.length} generated slide component(s) → ${outPath}`);
