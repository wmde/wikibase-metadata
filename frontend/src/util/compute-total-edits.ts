type PartialWikibaseRecentChangesObservationSet = {
	mostRecent?: { botChangeCount?: number | null; humanChangeCount?: number | null } | null
}

const computeTotalEdits = (v: PartialWikibaseRecentChangesObservationSet): number | undefined =>
	(v.mostRecent?.botChangeCount != null && v.mostRecent?.botChangeCount != undefined) ||
	(v.mostRecent?.humanChangeCount != null && v.mostRecent?.humanChangeCount != undefined)
		? (v.mostRecent?.botChangeCount ?? 0) + (v.mostRecent?.humanChangeCount ?? 0)
		: undefined

export default computeTotalEdits
