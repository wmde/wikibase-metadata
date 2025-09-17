import type { Wikibase, ObsKind } from "../types";

// Dates
export function daysSince(dateIso?: string): number | null {
    if (!dateIso) return null;
    const t = new Date(dateIso).getTime();
    if (Number.isNaN(t)) return null;
    return Math.max(0, Math.floor((Date.now() - t) / 86400000));
}

export function relativeDaysText(dateIso?: string): string {
    const d = daysSince(dateIso);
    if (d == null) return "";
    if (d === 0) return "today";
    if (d === 1) return "yesterday";
    return `${d} days ago`;
}

// Staleness
export function isStaleFor(
    w: Wikibase,
    kind: ObsKind,
    thresholdDays = 30,
): boolean {
    const d = w.getObservationDate(kind);
    const ds = daysSince(d);
    return ds == null || ds > thresholdDays;
}

// Formatting
export function fmtOrDash(w: Wikibase, n?: number | null): string {
    return n == null ? "—" : w.fmt(n);
}

export function textOrDash(s?: string | null): string {
    return s && String(s).length > 0 ? String(s) : "—";
}

// Observation helpers
export function obsHeadline(w: Wikibase, kind: ObsKind): string {
    const d = w.getObservationDate(kind);
    const rel = relativeDaysText(d);
    return rel ? `Fetched ${rel}` : "No data";
}
