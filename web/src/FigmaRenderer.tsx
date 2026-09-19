import { useMemo } from "react";
import { figmaNodeToStyle, type FigmaNode } from "./figmaToReact";

interface Props {
  node: FigmaNode;
  /** Scale the rendered root to fit this width in px. */
  fitWidth?: number;
}

/**
 * Live-render a Figma node tree (REST API model) as React/CSS.
 * Same mapping as scripts/figma-to-react.mjs — so what you see here
 * is what the generator commits.
 */
function NodeView({ node, parent }: { node: FigmaNode; parent?: FigmaNode }) {
  if (node.visible === false) return null;
  const style = figmaNodeToStyle(node, parent);

  if (node.type === "TEXT") {
    return (
      <p
        data-node={node.id}
        data-name={node.name}
        style={{ ...style, margin: 0 }}
      >
        {node.characters}
      </p>
    );
  }

  const children = (node.children ?? []).filter((c) => c.visible !== false);
  if (!children.length) {
    const isVector = node.type === "VECTOR" || node.type === "BOOLEAN_OPERATION";
    return (
      <div
        data-node={node.id}
        data-name={node.name}
        style={{
          ...style,
          ...(isVector
            ? {
                border: "1px dashed rgba(37, 99, 235, 0.45)",
                background: "rgba(56, 189, 248, 0.08)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }
            : {}),
        }}
        title={isVector ? `${node.name} — export via GET /v1/images/:key` : node.name}
      >
        {isVector && (
          <span style={{ fontSize: 9, color: "var(--ink-faint)", fontFamily: "var(--font)" }}>
            {node.name}
          </span>
        )}
      </div>
    );
  }
  return (
    <div data-node={node.id} data-name={node.name} style={style}>
      {children.map((c) => (
        <NodeView key={c.id} node={c} parent={node} />
      ))}
    </div>
  );
}

export default function FigmaRenderer({ node, fitWidth }: Props) {
  const scale = useMemo(() => {
    if (!fitWidth) return 1;
    const w = node.absoluteBoundingBox?.width ?? 0;
    return w ? Math.min(1, fitWidth / w) : 1;
  }, [fitWidth, node]);

  const h = (node.absoluteBoundingBox?.height ?? 0) * scale;
  return (
    <div style={{ width: "100%", overflow: "hidden", pointerEvents: "none" }}>
      <div
        style={{
          transform: `scale(${scale})`,
          transformOrigin: "top left",
          height: h,
        }}
      >
        <NodeView node={node} />
      </div>
    </div>
  );
}
