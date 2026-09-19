// Client-side Figma REST API client.
//
// The Figma API can only be called from a browser that can reach
// api.figma.com (this dev sandbox's egress does not allow it, but your
// local browser does). The token is read from VITE_FIGMA_TOKEN
// (web/.env.local — gitignored) and can be overridden in the Figma panel.

const FIGMA_API = "https://api.figma.com/v1";

export const DEFAULT_FIGMA_TOKEN: string =
  (import.meta.env.VITE_FIGMA_TOKEN as string | undefined) ?? "";

export interface FigmaNodeSummary {
  id: string;
  name: string;
  type: string;
  depth: number;
}

async function figmaFetch(path: string, token: string): Promise<any> {
  const res = await fetch(`${FIGMA_API}${path}`, {
    headers: { "X-Figma-Token": token },
  });
  if (!res.ok) {
    let detail = `${res.status} ${res.statusText}`;
    try {
      const body = await res.json();
      if (body && body.error) detail = body.error;
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return res.json();
}

export interface FigmaFileDoc {
  name: string;
  lastModified: string;
  pages: { id: string; name: string }[];
  nodes: FigmaNodeSummary[];
  /** The raw full document response (complete node tree for live rendering). */
  full: any;
}

/** Fetch a file's full document (needed by FigmaRenderer for fills/styles) and a flat node list. */
export async function fetchFigmaFile(fileKey: string, token: string): Promise<FigmaFileDoc> {
  const data = await figmaFetch(`/files/${encodeURIComponent(fileKey)}`, token);
  const pages: { id: string; name: string }[] = [];
  const nodes: FigmaNodeSummary[] = [];
  const doc = data.document;
  if (doc) {
    for (const page of doc.children ?? []) {
      pages.push({ id: page.id, name: page.name });
      for (const child of page.children ?? []) {
        nodes.push({ id: child.id, name: child.name, type: child.type, depth: 1 });
        for (const grand of child.children ?? []) {
          nodes.push({ id: grand.id, name: grand.name, type: grand.type, depth: 2 });
        }
      }
    }
  }
  return { name: data.name ?? "Figma file", lastModified: data.lastModified ?? "", pages, nodes, full: data };
}

/** Render a specific node (or the whole file) to a PNG; returns an image URL (valid ~1h). */
export async function renderFigmaNode(
  fileKey: string,
  nodeId: string,
  token: string,
  scale = 1
): Promise<string> {
  const idParam = nodeId && nodeId !== "root" ? `&ids=${encodeURIComponent(nodeId)}` : "";
  const data = await figmaFetch(`/images/${encodeURIComponent(fileKey)}?format=png&scale=${scale}${idParam}`, token);
  const id = nodeId && nodeId !== "root" ? nodeId : "root";
  const url = data.imgs?.[id] ?? Object.values(data.imgs ?? {})[0];
  if (!url) throw new Error("Figma did not return an image URL for the requested node.");
  return url;
}

/** Extract a file key (and optional node id) from a pasted Figma URL or raw key. */
export function parseFigmaInput(input: string): { fileKey: string; nodeId: string } {
  const trimmed = input.trim();
  if (trimmed.includes("figma.com/")) {
    try {
      const u = new URL(trimmed.startsWith("http") ? trimmed : `https://${trimmed}`);
      const parts = u.pathname.split("/").filter(Boolean);
      const fileKey = parts[1] ?? "";
      let nodeId = "";
      if (u.searchParams.get("node-id")) {
        nodeId = u.searchParams.get("node-id")!.replace(/-/g, ":");
      } else {
        const ni = parts.indexOf("node-id");
        if (ni >= 0 && parts[ni + 1]) nodeId = parts[ni + 1].replace(/-/g, ":");
      }
      return { fileKey, nodeId };
    } catch {
      return { fileKey: "", nodeId: "" };
    }
  }
  return { fileKey: trimmed, nodeId: "" };
}
