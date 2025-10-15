type PartialWikibaseRecentChangesObservationSet = {
	mostRecent?: {
		botChangeCount?: number
		humanChangeCount?: number
	} | null
}

const computeTotalEdits = (v: PartialWikibaseRecentChangesObservationSet): number | undefined =>
	v.mostRecent?.botChangeCount != undefined || v.mostRecent?.humanChangeCount != undefined
		? (v.mostRecent?.botChangeCount ?? 0) + (v.mostRecent?.humanChangeCount ?? 0)
		: undefined

export default computeTotalEdits
