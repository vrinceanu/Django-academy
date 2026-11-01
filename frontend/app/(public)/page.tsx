import Link from "next/link";

import { ChipMark, Wordmark } from "@/components/ChipMark";

import styles from "./home.module.css";

const STEPS = [
  {
    title: "Apply for a cohort",
    body: "Pick a microcredential for the coming Network cycle. An admin confirms your seat.",
  },
  {
    title: "Work through the workshops",
    body: "Recorded lectures, readings, quizzes and assignments, with an instructor for your cohort.",
  },
  {
    title: "Earn a verifiable badge",
    body: "Meet the pass mark and receive a signed badge and certificate that member schools recognize.",
  },
];

export default function Home() {
  return (
    <div className={styles.page}>
      <header className={styles.hero}>
        <div className={styles.heroInner}>
          <Link href="/" className={styles.brand} aria-label="CHIPS Academy home">
            <ChipMark size={40} />
            <Wordmark />
          </Link>
          <div className={styles.heroBody}>
            <div>
              <h1 className={styles.title}>
                Microcredentials in semiconductors and microelectronics
              </h1>
              <p className={styles.lede}>
                Short, cohort-based workshops taught across the HBCU CHIPS Network, for junior and
                senior engineering students.
              </p>
              <Link href="/learn" className="button">
                Sign in with your Network account
              </Link>
            </div>
            <div className={styles.art} aria-hidden="true">
              <svg viewBox="0 0 320 320" className={styles.traces}>
                <g fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                  <path d="M137.5 92.5V48H70V12" />
                  <path d="M160.0 92.5V20H250" />
                  <path d="M182.5 92.5V58" />
                  <path d="M227.5 137.5H288V52" />
                  <path d="M227.5 160.0H306" />
                  <path d="M227.5 182.5H296V270" />
                  <path d="M137.5 227.5V296H92" />
                  <path d="M182.5 227.5V284H306" />
                  <path d="M92.5 137.5H22" />
                  <path d="M92.5 182.5H32V300" />
                </g>
                <g fill="currentColor">
                  <circle cx="70" cy="12" r="5" />
                  <circle cx="250" cy="20" r="5" />
                  <circle cx="182.5" cy="58" r="5" />
                  <circle cx="288" cy="52" r="5" />
                  <circle cx="306" cy="160.0" r="5" />
                  <circle cx="296" cy="270" r="5" />
                  <circle cx="92" cy="296" r="5" />
                  <circle cx="306" cy="284" r="5" />
                  <circle cx="22" cy="137.5" r="5" />
                  <circle cx="32" cy="300" r="5" />
                </g>
              </svg>
              <div className={styles.chip}>
                <ChipMark size={180} />
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className={styles.main}>
        <h2>How it works</h2>
        <ol className={styles.steps}>
          {STEPS.map((step) => (
            <li key={step.title}>
              <h3>{step.title}</h3>
              <p>{step.body}</p>
            </li>
          ))}
        </ol>
      </main>

      <footer className={styles.footer}>
        <p>CHIPS Academy is run by the HBCU CHIPS Network.</p>
      </footer>
    </div>
  );
}
