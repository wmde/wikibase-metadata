import type { Wikibase, ObsKind } from "./types";

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
const nf = new Intl.NumberFormat(undefined);

export function formatNumber(n?: number | null): string {
	if (n == null) return "";
	try {
		return nf.format(n as number);
	} catch {
		return String(n);
	}
}

export function fmtOrDash(_w: Wikibase, n?: number | null): string {
	return n == null ? "—" : formatNumber(n);
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

export function formatDate(s?: string): string {
	if (!s) return "";
	const d = new Date(s);
	return Number.isNaN(d.getTime()) ? s : d.toLocaleDateString();
}
