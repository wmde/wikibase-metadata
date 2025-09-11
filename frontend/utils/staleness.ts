import type { Wikibase, ObsKind } from "../types";
import { daysSince } from "./datetime";

export function isStaleFor(
	w: Wikibase,
	kind: ObsKind,
	thresholdDays = 30,
): boolean {
	const d = w.getObservationDate(kind);
	const ds = daysSince(d);
	return ds == null || ds > thresholdDays;
}
