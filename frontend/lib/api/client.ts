// Typed API client. `schema.d.ts` is generated from the Django OpenAPI schema
// (`npm run api:generate`); CI fails if it is out of date.
import createClient from "openapi-fetch";

import type { paths } from "./schema";

function readCookie(name: string): string | undefined {
  if (typeof document === "undefined") return undefined;
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith(`${name}=`))
    ?.split("=")[1];
}

export const api = createClient<paths>({ baseUrl: "", credentials: "include" });

api.use({
  onRequest({ request }) {
    const token = readCookie("csrftoken");
    if (token && request.method !== "GET") request.headers.set("X-CSRFToken", token);
    return request;
  },
});
