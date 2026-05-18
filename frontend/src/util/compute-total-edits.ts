type PartialWikibaseRecentChangesObservation = {
	botChangeCount?: number | null
	humanChangeCount?: number | null
}

const computeTotalEdits = (
	v: PartialWikibaseRecentChangesObservation | null | undefined
): number | undefined =>
	(v?.botChangeCount != null && v.botChangeCount != undefined) ||
	(v?.humanChangeCount != null && v.humanChangeCount != undefined)
		? (v.botChangeCount ?? 0) + (v.humanChangeCount ?? 0)
		: undefined

export default computeTotalEdits
