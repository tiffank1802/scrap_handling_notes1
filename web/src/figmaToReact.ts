/* ============================================================
   figmaToReact — Figma node-tree → React (styles + JSX)
   ----------------------------------------------------------
   Maps the Figma REST API node model (GET /v1/files/:key) onto
   React inline styles + JSX. The same mapping is mirrored in
   scripts/figma-to-react.mjs (the Node generator that uses the
   `figma-api` package) so that the committed generated output
   matches what this module emits.

   Supported node types: FRAME, GROUP, INSTANCE, COMPONENT,
   SECTION, RECTANGLE, ELLIPSE, LINE, TEXT.
   Vectors / boolean ops are emitted as labelled placeholders —
   export them as images via GET /v1/images/:key when needed.
   ============================================================ */

export interface FigmaColor {
  r: number;
  g: number;
  b: number;
  a?: number;
}

export type FigmaNode = {
  id: string;
  name: string;
  type: string;
  visible?: boolean;
  opacity?: number;
  absoluteBoundingBox?: { x: number; y: number; width: number; height: number };
  fills?: any[];
  strokes?: any[];
  strokeWeight?: number;
  cornerRadius?: number;
  rectangleCornerRadii?: number[];
  effects?: any[];
  layoutMode?: "HORIZONTAL" | "VERTICAL" | "NONE";
  itemSpacing?: number;
  paddingLeft?: number;
  paddingRight?: number;
  paddingTop?: number;
  paddingBottom?: number;
  primaryAxisAlignItems?: string;
  counterAxisAlignItems?: string;
  layoutWrap?: string;
  clipsContent?: boolean;
  characters?: string;
  style?: {
    fontFamily?: string;
    fontWeight?: number;
    fontSize?: number;
    letterSpacing?: number;
    lineHeightPx?: number;
    textAlignHorizontal?: string;
  };
  children?: FigmaNode[];
};

const cssColor = (c: FigmaColor): string => {
  const r = Math.round(c.r * 255);
  const g = Math.round(c.g * 255);
  const b = Math.round(c.b * 255);
  const a = c.a ?? 1;
  return a >= 1 ? `rgb(${r}, ${g}, ${b})` : `rgba(${r}, ${g}, ${b}, ${a})`;
};

function gradientToCss(fill: any): string {
  const stops = (fill.gradientStops ?? [])
    .map((s: any) => `${cssColor(s.color)} ${(s.position * 100).toFixed(1)}%`)
    .join(", ");
  let angle = 90;
  const h = fill.gradientHandlePositions;
  if (h && h[0] && h[1]) {
    const dx = h[1].x - h[0].x;
    const dy = h[1].y - h[0].y;
    angle = (Math.atan2(dy, dx) * 180) / Math.PI + 90;
  }
  return `linear-gradient(${angle.toFixed(1)}deg, ${stops})`;
}

function fillsToBackground(fills?: any[]): string | undefined {
  if (!fills || fills.length === 0) return undefined;
  const layers: string[] = [];
  for (const f of fills) {
    if (f.visible === false) continue;
    if (f.type === "SOLID" && f.color) {
      layers.unshift(cssColor(f.color));
      if (f.opacity !== undefined && f.opacity !== 1) {
        // re-encode with opacity
        const c = { ...f.color, a: (f.color.a ?? 1) * f.opacity };
        layers[0] = cssColor(c);
      }
    } else if (f.type === "GRADIENT_LINEAR" || f.type === "GRADIENT_RADIAL") {
      layers.unshift(gradientToCss(f));
    }
    // IMAGE fills need GET /v1/images — left as placeholders
  }
  return layers.length ? layers.join(", ") : undefined;
}

function effectsToCss(node: FigmaNode): Partial<Record<string, string>> {
  const out: Partial<Record<string, string>> = {};
  const shadows: string[] = [];
  for (const e of node.effects ?? []) {
    if (e.visible === false) continue;
    if (e.type === "DROP_SHADOW" && e.color) {
      const c = e.color;
      shadows.push(
        `${e.offset?.x ?? 0}px ${e.offset?.y ?? 0}px ${e.radius ?? 0}px ${e.spread ?? 0}px ${cssColor(c)}`
      );
    } else if (e.type === "BACKGROUND_BLUR") {
      out.backdropFilter = `blur(${e.radius ?? 0}px)`;
      out.WebkitBackdropFilter = `blur(${e.radius ?? 0}px)`;
    } else if (e.type === "LAYER_BLUR") {
      out.filter = `blur(${e.radius ?? 0}px)`;
    }
  }
  if (shadows.length) out.boxShadow = shadows.join(", ");
  return out;
}

const ALIGN: Record<string, string> = {
  MIN: "flex-start",
  CENTER: "center",
  MAX: "flex-end",
  SPACE_BETWEEN: "space-between",
};

/** Convert a Figma node into a React style object (px units). */
export function figmaNodeToStyle(node: FigmaNode, parent?: FigmaNode): Record<string, any> {
  const style: Record<string, any> = {};
  const bb = node.absoluteBoundingBox;
  if (node.opacity !== undefined && node.opacity !== 1) style.opacity = node.opacity;

  const autoLayout = node.layoutMode === "HORIZONTAL" || node.layoutMode === "VERTICAL";

  if (autoLayout) {
    style.display = "flex";
    style.flexDirection = node.layoutMode === "HORIZONTAL" ? "row" : "column";
    if (node.itemSpacing !== undefined) style.gap = node.itemSpacing;
    const p = [node.paddingTop, node.paddingRight, node.paddingBottom, node.paddingLeft].filter(
      (v) => v !== undefined
    );
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
  if (node.strokes?.length && node.strokes[0]?.visible !== false && node.strokes[0]?.color) {
    style.border = `${node.strokeWeight ?? 1}px solid ${cssColor(node.strokes[0].color)}`;
  }
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

const esc = (s: string) =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const styleLiteral = (style: Record<string, any>): string => {
  const entries = Object.entries(style)
    .map(([k, v]) => {
      const key = /^[A-Za-z_$][A-Za-z0-9_$]*$/.test(k) ? k : JSON.stringify(k);
      return `${key}: ${typeof v === "string" ? JSON.stringify(v) : v}`;
    })
    .join(", ");
  return `{${entries}}`;
};

/** Serialize a Figma node tree into React JSX (string). */
export function figmaTreeToJsx(node: FigmaNode, indent = 0, parent?: FigmaNode): string {
  if (node.visible === false) return `/* hidden node ${node.name} */\n`;
  const pad = "  ".repeat(indent);
  const attrs = `data-node="${node.id}" data-name="${esc(node.name)}"`;

  if (node.type === "TEXT") {
    const style = figmaNodeToStyle(node, parent);
    const text = esc(node.characters ?? "");
    if (indent === 0) {
      return `export default function FigmaNode() {\n  return (\n    <div ${attrs} style={${styleLiteral(style)}}>\n      <p style={{margin: 0}}>${text}</p>\n    </div>\n  );\n}\n`;
    }
    return `${pad}<p ${attrs} style={${styleLiteral(style)}}>${text}</p>\n`;
  }

  const style = figmaNodeToStyle(node, parent);
  const isContainer = (node.children ?? []).length > 0;
  if (!isContainer) {
    const tag = "div";
    return `${pad}<${tag} ${attrs} style={${styleLiteral(style)}} />\n`;
  }

  const children = (node.children ?? [])
    .map((c) => figmaTreeToJsx(c, indent + 1, node))
    .join("");
  if (indent === 0) {
    return `// Generated from Figma node ${node.id} — "${node.name}"\nexport default function FigmaNode() {\n  return (\n    <div ${attrs} style={${styleLiteral(style)}}>\n${children}    </div>\n  );\n}\n`;
  }
  return `${pad}<div ${attrs} style={${styleLiteral(style)}}>\n${children}${pad}</div>\n`;
}

/** Find the slide frames (top-level frames under pages) of a file document. */
export function findSlideFrames(document: any): FigmaNode[] {
  const frames: FigmaNode[] = [];
  for (const page of document?.children ?? []) {
    if (page.type === "PAGE") {
      for (const child of page.children ?? []) {
        if (child.type === "FRAME" || child.type === "INSTANCE") frames.push(child);
      }
    }
  }
  return frames.length ? frames : (document?.children ?? []).filter((c: any) => c.type === "FRAME");
}
