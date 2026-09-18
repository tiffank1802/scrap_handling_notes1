import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    // The Arena live preview proxies through a per-sandbox host
    // (e.g. https://5173-<sandboxId>.e2b.app) — allow all preview hosts.
    allowedHosts: true,
  },
});
