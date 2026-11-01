import type { Metadata } from "next";

import { ScreenPlaceholder } from "@/components/ScreenPlaceholder";
import { SCREENS } from "@/components/screens";

type Props = { params: Promise<{ slug?: string[] }> };

function pathFor(slug?: string[]): string {
  return ["/studio", ...(slug ?? [])].join("/");
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  return { title: SCREENS[pathFor(slug)]?.title ?? "Not found" };
}

export default async function Page({ params }: Props) {
  const { slug } = await params;
  return <ScreenPlaceholder path={pathFor(slug)} />;
}
