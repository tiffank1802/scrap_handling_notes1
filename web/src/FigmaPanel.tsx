import { useMemo, useState, type ReactNode } from "react";
import {
  DEFAULT_FIGMA_TOKEN,
  fetchFigmaFile,
  parseFigmaInput,
  renderFigmaNode,
  type FigmaFileDoc,
} from "./figma";
import FigmaRenderer from "./FigmaRenderer";
import { figmaTreeToJsx, findSlideFrames, type FigmaNode } from "./figmaToReact";
import sampleFile from "../scripts/sample-slide.json";
import { GENERATED_SLIDES } from "./figma/generated/slides.generated";

interface Props {
  onClose: () => void;
}

const PANEL_W = 460;
const PAD = 24;
const FIT_W = PANEL_W - PAD * 2;

/** The committed generated slide (proof that the pipeline runs end-to-end). */
const SampleSlide = GENERATED_SLIDES[0]?.component ?? null;

function Scaled({ children, w }: { children: ReactNode; w: number }) {
  const s = Math.min(1, FIT_W / w);
  return (
    <div style={{ overflow: "hidden" }}>
      <div style={{ transform: `scale(${s})`, transformOrigin: "top left", height: 720 * s, width: w * s }}>
        {children}
      </div>
    </div>
  );
}

/**
 * Figma bridge — Figma components → live React.
 * Loads a Figma file via the REST API (or the bundled sample), renders its
 * node tree as React/CSS, and exports the generated React code.
 */
export default function FigmaPanel({ onClose }: Props) {
  const [token, setToken] = useState(DEFAULT_FIGMA_TOKEN);
  const [input, setInput] = useState("");
  const [doc, setDoc] = useState<FigmaFileDoc | null>(null);
  const [fileKey, setFileKey] = useState("");
  const [source, setSource] = useState<any | null>(null);
  const [sourceLabel, setSourceLabel] = useState("");
  const [frameIdx, setFrameIdx] = useState(0);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState(false);
  const [imgUrl, setImgUrl] = useState("");
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState(false);

  const frames = useMemo<FigmaNode[]>(() => (source ? findSlideFrames(source.document ?? source) : []), [source]);
  const frame = frames[Math.min(frameIdx, frames.length - 1)];

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

  function loadSample() {
    setSource(sampleFile);
    setSourceLabel("Bundled sample (scripts/sample-slide.json)");
    setFrameIdx(0);
    setImgUrl("");
    say("Sample loaded — node tree rendered below, generated code committed in src/figma/generated/.");
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

  const generatedCode = useMemo(() => (frame ? figmaTreeToJsx(frame) : ""), [frame]);

  async function copyCode() {
    try {
      await navigator.clipboard.writeText(generatedCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      say("Clipboard blocked — select the code in the <details> below instead.", true);
    }
  }

  function downloadCode() {
    const blob = new Blob([generatedCode], { type: "text/javascript" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "figma-slide.generated.tsx";
    a.click();
    URL.revokeObjectURL(a.href);
  }

  return (
    <div className="figma-panel">
      <div className="head" style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <h3>Figma → React bridge</h3>
        <button className="icon-btn" onClick={onClose}>✕ close</button>
      </div>

      <div className="row" style={{ gap: 8 }}>
        <button className="icon-btn" onClick={loadSample}>▶ Load bundled sample</button>
        <span className="figma-msg" style={{ alignSelf: "center" }}>— or load your file —</span>
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
        REST calls run in your browser (<code>figma-api</code> surface): <code>GET /v1/files/:key</code> →
        node tree → live React render + generated code. The committed generator
        (<code>scripts/figma-to-react.mjs</code>) does the same in Node against your real file.
      </p>

      {msg && <p className={`figma-msg ${err ? "err" : ""}`}>{msg}</p>}

      {doc && (
        <div>
          <label>Top-level nodes — click to render PNG</label>
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

      {doc && (
        <div>
          <label>Figma node as PNG</label>
          <div className="figma-preview" style={{ marginTop: 5 }}>
            {busy ? <div className="empty">Rendering…</div>
              : imgUrl ? <img src={imgUrl} alt="Figma node render" />
              : <div className="empty">Select a node above to render a PNG reference from Figma.</div>}
          </div>
        </div>
      )}

      {frame && (
        <>
          {frames.length > 1 && (
            <div>
              <label>Slide frame</label>
              <select value={frameIdx} onChange={(e) => setFrameIdx(Number(e.target.value))} style={{ marginTop: 5 }}>
                {frames.map((f, i) => (
                  <option key={f.id} value={i}>{i + 1}. {f.name}</option>
                ))}
              </select>
            </div>
          )}

          <div>
            <label>Live render — Figma node tree → React (same mapping as the generator)</label>
            <div className="figma-preview" style={{ marginTop: 5, minHeight: 120, padding: 8 }}>
              <Scaled w={frame.absoluteBoundingBox?.width ?? 1280}>
                <FigmaRenderer node={frame} />
              </Scaled>
            </div>
          </div>

          <div className="row" style={{ gap: 8 }}>
            <button className="icon-btn" onClick={copyCode}>{copied ? "✓ Copied" : "⧉ Copy React code"}</button>
            <button className="icon-btn" onClick={downloadCode}>↓ Download .tsx</button>
          </div>

          <details>
            <summary style={{ cursor: "pointer", fontSize: 12, fontWeight: 700, color: "var(--ink-soft)" }}>
              Generated React code (from Figma data)
            </summary>
            <pre style={{
              marginTop: 8,
              fontSize: 10,
              lineHeight: 1.5,
              background: "rgba(22, 40, 60, 0.04)",
              border: "1px solid rgba(190, 214, 236, 0.7)",
              borderRadius: 10,
              padding: 10,
              overflow: "auto",
              maxHeight: 260,
              whiteSpace: "pre-wrap",
              wordBreak: "break-all",
            }}>
              {generatedCode}
            </pre>
          </details>
        </>
      )}

      {SampleSlide && sourceLabel.includes("sample") && (
        <div>
          <label>Committed generated output — src/figma/generated/</label>
          <p className="figma-msg" style={{ marginTop: 0 }}>
            <code>{SampleSlide.name}</code> was written by{" "}
            <code>scripts/figma-to-react.mjs</code> from <code>scripts/sample-slide.json</code> and is
            part of this repo — identical to the live render above.
          </p>
          <div className="figma-preview" style={{ marginTop: 5, padding: 8 }}>
            <Scaled w={1280}>
              <SampleSlide />
            </Scaled>
          </div>
        </div>
      )}
    </div>
  );
}
