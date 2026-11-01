"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, type ReactNode } from "react";

import { ChipMark, Wordmark } from "./ChipMark";
import { ACCOUNT_ITEMS, AREAS, type NavItem } from "./nav";
import styles from "./AppShell.module.css";

function isActive(pathname: string, href: string, areaHome: string): boolean {
  if (href === areaHome) return pathname === href;
  return pathname === href || pathname.startsWith(`${href}/`);
}

export function AppShell({ area, children }: { area: string; children: ReactNode }) {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const current = AREAS.find((a) => a.key === area);
  const home = current?.home ?? "/account";
  const items: NavItem[] = current?.items ?? ACCOUNT_ITEMS;

  return (
    <div className={styles.shell}>
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <header className={styles.topbar}>
        <Link href="/" className={styles.brand} aria-label="CHIPS Academy home">
          <ChipMark size={30} />
          <Wordmark />
        </Link>
        <button
          type="button"
          className={styles.menuButton}
          aria-expanded={open}
          aria-controls="rail"
          onClick={() => setOpen((v) => !v)}
        >
          {open ? "Close menu" : "Menu"}
        </button>
      </header>

      <nav id="rail" className={styles.rail} data-open={open} aria-label="Main">
        <Link href="/" className={`${styles.brand} ${styles.railBrand}`} aria-label="CHIPS Academy home">
          <ChipMark size={36} />
          <Wordmark />
        </Link>

        <ul className={styles.areas} aria-label="Areas">
          {AREAS.map((a) => (
            <li key={a.key}>
              <Link
                href={a.home}
                className={styles.area}
                aria-current={a.key === area ? "true" : undefined}
                onClick={() => setOpen(false)}
              >
                {a.label}
              </Link>
            </li>
          ))}
        </ul>

        <ul className={styles.items}>
          {items.map((item) => {
            const active = isActive(pathname, item.href, home);
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={styles.item}
                  aria-current={active ? "page" : undefined}
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>

        <ul className={`${styles.items} ${styles.account}`} aria-label="Account">
          {ACCOUNT_ITEMS.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className={styles.item}
                aria-current={pathname === item.href ? "page" : undefined}
                onClick={() => setOpen(false)}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      <main id="main" className={styles.main}>
        {children}
      </main>
    </div>
  );
}
