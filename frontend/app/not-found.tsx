import Link from "next/link";

export default function NotFound() {
  return (
    <main style={{ padding: "64px 24px", maxWidth: "60ch", margin: "0 auto" }}>
      <h1>Page not found</h1>
      <p>This address is not part of CHIPS Academy.</p>
      <Link href="/" className="button">
        Go to the home page
      </Link>
    </main>
  );
}
