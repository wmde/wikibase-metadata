import type { Wikibase } from "../types";

export function fmtOrDash(w: Wikibase, n?: number | null): string {
  return n == null ? "—" : w.fmt(n);
}

export function textOrDash(s?: string | null): string {
  return s && String(s).length > 0 ? String(s) : "—";
}

