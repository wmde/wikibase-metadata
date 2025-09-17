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
