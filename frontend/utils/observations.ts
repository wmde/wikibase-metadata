import type { Wikibase, ObsKind } from "../types";
import { relativeDaysText } from "./datetime";

export function obsHeadline(w: Wikibase, kind: ObsKind): string {
  const d = w.getObservationDate(kind);
  const rel = relativeDaysText(d);
  return rel ? `Fetched ${rel}` : "No data";
}

