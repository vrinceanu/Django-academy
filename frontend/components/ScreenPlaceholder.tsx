import { SCREENS } from "./screens";
import styles from "./ScreenPlaceholder.module.css";

export function ScreenPlaceholder({ path }: { path: string }) {
  const screen = SCREENS[path];
  if (!screen) {
    return (
      <section>
        <h1>Page not found</h1>
        <p>This address is not part of CHIPS Academy. Use the menu to find your way back.</p>
      </section>
    );
  }
  return (
    <section className={styles.placeholder}>
      <h1>{screen.title}</h1>
      <p className={styles.summary}>{screen.summary}</p>
      <p className={styles.status}>
        This screen is built in milestone {screen.milestone}. It is listed here so the navigation can
        be reviewed on staging.
      </p>
    </section>
  );
}
