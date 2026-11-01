import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "CHIPS Academy",
    short_name: "CHIPS",
    description: "HBCU CHIPS Network microcredentials",
    start_url: "/learn",
    display: "standalone",
    background_color: "#04101f",
    theme_color: "#04101f",
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
  };
}
