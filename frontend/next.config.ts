import type { NextConfig } from "next";

// In development the browser talks to Next on :3000 and Next forwards /api and
// /ops to Django, so cookies stay same-origin. In staging Caddy does the routing.
const apiOrigin = process.env.API_ORIGIN ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  poweredByHeader: false,
  async rewrites() {
    if (process.env.NODE_ENV === "production") return [];
    return [
      { source: "/api/:path*", destination: `${apiOrigin}/api/:path*` },
      { source: "/ops/:path*", destination: `${apiOrigin}/ops/:path*` },
    ];
  },
};

export default nextConfig;
