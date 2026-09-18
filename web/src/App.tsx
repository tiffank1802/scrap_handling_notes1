import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { SLIDES } from "./slides";
import { SLIDE_NOTES } from "./notes";
import FigmaPanel from "./FigmaPanel";

const STAGE_W = 1280;
const STAGE_H = 720;

export default function App() {
  const [idx, setIdx] = useState(0);
  const [scale, setScale] = useState(1);
  const [showGrid, setShowGrid] = useState(false);
  const [showNotes, setShowNotes] = useState(false);
  const [showFigma, setShowFigma] = useState(false);
  const viewportRef = useRef<HTMLDivElement>(null);

  const last = SLIDES.length - 1;
  const go = useCallback((n: number) => setIdx(Math.max(0, Math.min(last, n))), [last]);
  const next = useCallback(() => setIdx((i) => Math.min(last, i + 1)), [last]);
  const prev = useCallback(() => setIdx((i) => Math.max(0, i - 1)), []);

  // fit stage into viewport
  useEffect(() => {
    function fit() {
      const el = viewportRef.current;
      if (!el) return;
      const { width, height } = el.getBoundingClientRect();
      const s = Math.min((width - 32) / STAGE_W, (height - 24) / STAGE_H);
      setScale(Math.min(s, 1.6));
    }
    fit();
    window.addEventListener("resize", fit);
    return () => window.removeEventListener("resize", fit);
  }, []);

  // keyboard controls
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      switch (e.key) {
        case "ArrowRight":
        case "ArrowDown":
        case "PageDown":
        case " ":
          e.preventDefault();
          next();
          break;
        case "ArrowLeft":
        case "ArrowUp":
        case "PageUp":
          e.preventDefault();
          prev();
          break;
        case "Home":
          e.preventDefault();
          go(0);
          break;
        case "End":
          e.preventDefault();
          go(last);
          break;
        case "g":
        case "G":
        case "Escape":
          setShowGrid((v) => (e.key === "Escape" ? false : !v));
          break;
        case "n":
        case "N":
          setShowNotes((v) => !v);
          break;
        case "f":
        case "F":
          setShowFigma((v) => !v);
          break;
        case "t":
        case "T":
          go(0);
          break;
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [next, prev, go, last]);

  const note = useMemo(() => SLIDE_NOTES[idx], [idx]);
  const current = SLIDES[idx];

  function toggleFullscreen() {
    if (document.fullscreenElement) void document.exitFullscreen();
    else void document.documentElement.requestFullscreen().catch(() => undefined);
  }

  return (
    <div className="app">
      <div className="stage-viewport" ref={viewportRef}>
        <div className="stage" style={{ transform: `scale(${scale})` }}>
          <div key={idx} style={{ position: "absolute", inset: 0, animation: "fade-in 240ms ease" }}>
            {current.component()}
          </div>
        </div>
      </div>

      <div className="controls">
        <button className="icon-btn" onClick={() => setShowGrid(true)} title="Overview (G)">
          ▦ Overview
        </button>
        <button className={`icon-btn ${showNotes ? "active" : ""}`} onClick={() => setShowNotes((v) => !v)} title="Speaker notes (N)">
          ✎ Notes
        </button>
        <div
          className="progress"
          title="Jump to slide"
          onClick={(e) => {
            const r = (e.currentTarget as HTMLDivElement).getBoundingClientRect();
            go(Math.round(((e.clientX - r.left) / r.width) * last));
          }}
        >
          <div style={{ width: `${((idx + 1) / SLIDES.length) * 100}%` }} />
        </div>
        <span className="counter">
          {idx + 1} / {SLIDES.length}
        </span>
        <button className="icon-btn nav" onClick={prev} disabled={idx === 0} title="Previous (←)">‹</button>
        <button className="icon-btn nav" onClick={next} disabled={idx === last} title="Next (→)">›</button>
        <button className={`icon-btn ${showFigma ? "active" : ""}`} onClick={() => setShowFigma((v) => !v)} title="Figma bridge (F)">
          ◇ Figma
        </button>
        <button className="icon-btn" onClick={toggleFullscreen} title="Fullscreen">⛶</button>
      </div>

      {showGrid && (
        <div className="overlay" onClick={() => setShowGrid(false)}>
          <h2>Overview — {SLIDES.length} slides</h2>
          <div className="grid">
            {SLIDES.map((s, i) => (
              <div
                key={s.id}
                className={`tile ${i === idx ? "current" : ""}`}
                onClick={(e) => {
                  e.stopPropagation();
                  go(i);
                  setShowGrid(false);
                }}
              >
                <div className="n">{String(i + 1).padStart(2, "0")} · {s.kicker}</div>
                <div className="t">{s.label}</div>
                <div className="k">{i === idx ? "current slide" : "click to jump"}</div>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 11.5, color: "var(--ink-faint)" }}>
            Esc / click to close  ·  ← → space to navigate  ·  N notes  ·  F Figma
          </div>
        </div>
      )}

      {showNotes && note && (
        <aside className="notes-drawer">
          <div className="head">
            <h3>Speaker notes — slide {idx + 1}</h3>
            <button className="icon-btn" onClick={() => setShowNotes(false)}>✕</button>
          </div>
          <div className="body">{note.notes}</div>
          <div className="meta">
            Verbatim script from “Delft Phd scrap handling - completed.pptx” (15-minute interview flow).
          </div>
        </aside>
      )}

      {showFigma && <FigmaPanel onClose={() => setShowFigma(false)} />}
    </div>
  );
}
