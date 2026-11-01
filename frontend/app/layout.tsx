import type { Metadata, Viewport } from "next";
import localFont from "next/font/local";
import type { ReactNode } from "react";

import "./globals.css";

// IBM Plex Sans, self-hosted: no build-time network and no third-party font request.
const plex = localFont({
  src: [
    {
      path: "../node_modules/@fontsource/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2",
      weight: "400",
      style: "normal",
    },
    {
      path: "../node_modules/@fontsource/ibm-plex-sans/files/ibm-plex-sans-latin-500-normal.woff2",
      weight: "500",
      style: "normal",
    },
    {
      path: "../node_modules/@fontsource/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2",
      weight: "600",
      style: "normal",
    },
    {
      path: "../node_modules/@fontsource/ibm-plex-sans/files/ibm-plex-sans-latin-700-normal.woff2",
      weight: "700",
      style: "normal",
    },
  ],
  variable: "--font-plex",
  display: "swap",
});

export const metadata: Metadata = {
  title: { default: "CHIPS Academy", template: "%s · CHIPS Academy" },
  description:
    "Microcredentials in semiconductors and microelectronics from the HBCU CHIPS Network.",
  applicationName: "CHIPS Academy",
};

export const viewport: Viewport = {
  themeColor: "#04101f",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={plex.variable}>
      <body>{children}</body>
    </html>
  );
}
