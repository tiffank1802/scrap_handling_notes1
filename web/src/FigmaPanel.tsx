import { useState } from "react";
import {
  DEFAULT_FIGMA_TOKEN,
  fetchFigmaFile,
  parseFigmaInput,
  renderFigmaNode,
  type FigmaFileDoc,
} from "./figma";

interface Props {
  onClose: () => void;
}

/**
 * Figma bridge — a live window into the design file behind this deck.
 * Paste a Figma file URL (or file key) + your token, then render any
 * top-level node as a PNG reference. All calls run in the browser.
 */
export default function FigmaPanel({ onClose }: Props) {
  const [token, setToken] = useState(DEFAULT_FIGMA_TOKEN);
  const [input, setInput] = useState("");
  const [doc, setDoc] = useState<FigmaFileDoc | null>(null);
  const [fileKey, setFileKey] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState(false);
  const [imgUrl, setImgUrl] = useState("");
  const [busy, setBusy] = useState(false);

  function say(t: string, isErr = false) {
    setMsg(t);
    setErr(isErr);
  }

  async function load() {
    const { fileKey: key, nodeId } = parseFigmaInput(input);
    if (!key) return say("Paste a Figma file URL or file key first.", true);
    if (!token) return say("Enter your Figma personal access token first.", true);
    setLoading(true);
    setErr(false);
    say("");
    try {
      const d = await fetchFigmaFile(key, token);
      setDoc(d);
      setFileKey(key);
      say(`Loaded “${d.name}” — ${d.pages.length} page(s), ${d.nodes.length} top-level node(s).`);
      if (nodeId) void preview(nodeId, key);
    } catch (e) {
      say(`Figma API error: ${(e as Error).message}. Check the token & file access, and note: api.figma.com must be reachable from this browser.`, true);
    } finally {
      setLoading(false);
    }
  }

  async function preview(nodeId: string, key = fileKey) {
    if (!token) return say("Token missing.", true);
    setBusy(true);
    say("");
    try {
      const url = await renderFigmaNode(key, nodeId, token, 1);
      setImgUrl(url);
      say("Node rendered (Figma image URL is valid ~1 hour).");
    } catch (e) {
      say(`Render failed: ${(e as Error).message}`, true);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="figma-panel">
      <div className="head" style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <h3>Figma bridge</h3>
        <button className="icon-btn" onClick={onClose}>✕ close</button>
      </div>

      <div>
        <label>Figma file URL or key</label>
        <div style={{ display: "flex", gap: 8, marginTop: 5 }}>
          <input
            placeholder="https://www.figma.com/design/XXXX/…  or  XXXX"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button className="icon-btn" onClick={load} disabled={loading}>{loading ? "…" : "Load"}</button>
        </div>
      </div>

      <div>
        <label>Personal access token</label>
        <input
          type="password"
          placeholder="figd_…"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          style={{ marginTop: 5 }}
        />
      </div>

      <p className="figma-msg" style={{ marginTop: 0 }}>
        Reads <code>GET /v1/files/:key</code> and renders nodes via <code>GET /v1/images/:key</code>.
        Runs entirely in your browser — the token never leaves the page except to Figma.
      </p>

      {msg && <p className={`figma-msg ${err ? "err" : ""}`}>{msg}</p>}

      {doc && (
        <div>
          <label>Top-level nodes — click to render</label>
          <div className="node-tree" style={{ marginTop: 5 }}>
            {doc.pages.map((p) => (
              <div key={p.id} style={{ fontWeight: 800, color: "var(--ink)", marginTop: 6 }}>▸ {p.name}</div>
            ))}
            {doc.nodes.map((n) => (
              <div key={n.id} className="row" onClick={() => preview(n.id)}>
                <span style={{ paddingLeft: n.depth * 14 }} />
                <span className="kind">{n.type}</span>
                <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{n.name}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div>
        <label>Rendered node</label>
        <div className="figma-preview" style={{ marginTop: 5 }}>
          {busy ? <div className="empty">Rendering…</div>
            : imgUrl ? <img src={imgUrl} alt="Figma node render" />
            : <div className="empty">Select a node above to render a PNG reference from Figma here.</div>}
        </div>
      </div>
    </div>
  );
}
