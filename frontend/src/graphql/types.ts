/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> =
	T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never }
export type SortColumn = 'CATEGORY' | 'EDITS' | 'TITLE' | 'TRIPLES' | 'TYPE'

export type SortDirection = 'ASC' | 'DESC'

export type WikibaseCategory =
	| 'CULTURAL_AND_HISTORICAL'
	| 'DIGITAL_COLLECTIONS_AND_ARCHIVES'
	| 'EDUCATIONAL_AND_REFERENCE_COLLECTIONS'
	| 'EXPERIMENTAL_AND_PROTOTYPE_PROJECTS'
	| 'FICTIONAL_AND_CREATIVE_WORKS'
	| 'LEGAL_AND_POLITICAL'
	| 'LINGUISTIC_AND_LITERARY'
	| 'MATHEMATICS_AND_SCIENCE'
	| 'SEMANTIC_AND_PROSOPOGRAPHIC_DATA'
	| 'SOCIAL_AND_ADVOCACY'
	| 'TECHNOLOGY_AND_OPEN_SOURCE'

export type WikibaseFilterInput = {
	ignoreReuse?: boolean | null | undefined
	searchText?: string | null | undefined
	wikibaseType?: WikibaseTypeInput | null | undefined
}

export type WikibaseSortInput = {
	column: SortColumn
	dir: SortDirection
}

export type WikibaseType = 'CLOUD' | 'OTHER' | 'SUITE' | 'TEST' | 'UNKNOWN'

export type WikibaseTypeInput = {
	exclude?: Array<WikibaseType> | null | undefined
	include?: Array<WikibaseType> | null | undefined
}

export type SingleWikibaseQueryVariables = Exact<{
	wikibaseId: number
}>

export type SingleWikibaseQuery = {
	wikibase: {
		id: string
		title: string
		category: WikibaseCategory | null
		description: string | null
		wikibaseType: WikibaseType
		urls: { baseUrl: string; scriptPath: string | null; sparqlFrontendUrl: string | null }
		externalIdentifierObservations: {
			mostRecent: {
				id: string
				observationDate: Date
				totalExternalIdentifierStatements: number | null
			} | null
		}
		quantityObservations: {
			mostRecent: {
				id: string
				observationDate: Date
				totalItems: number | null
				totalLexemes: number | null
				totalProperties: number | null
				totalTriples: number | null
			} | null
		}
		recentChangesObservations: {
			mostRecent: {
				id: string
				observationDate: Date
				botChangeCount: number | null
				humanChangeCount: number | null
			} | null
		}
		timeToFirstValueObservations: {
			mostRecent: {
				id: string
				initiationDate: Date | null
				itemDates: Array<{ id: string; q: number; creationDate: Date }>
			} | null
		}
	}
}

export type SingleWikibaseFragment = {
	id: string
	title: string
	category: WikibaseCategory | null
	description: string | null
	wikibaseType: WikibaseType
	urls: { baseUrl: string; scriptPath: string | null; sparqlFrontendUrl: string | null }
	externalIdentifierObservations: {
		mostRecent: {
			id: string
			observationDate: Date
			totalExternalIdentifierStatements: number | null
		} | null
	}
	quantityObservations: {
		mostRecent: {
			id: string
			observationDate: Date
			totalItems: number | null
			totalLexemes: number | null
			totalProperties: number | null
			totalTriples: number | null
		} | null
	}
	recentChangesObservations: {
		mostRecent: {
			id: string
			observationDate: Date
			botChangeCount: number | null
			humanChangeCount: number | null
		} | null
	}
	timeToFirstValueObservations: {
		mostRecent: {
			id: string
			initiationDate: Date | null
			itemDates: Array<{ id: string; q: number; creationDate: Date }>
		} | null
	}
}

export type ListWikibasesQueryVariables = Exact<{ [key: string]: never }>

export type ListWikibasesQuery = {
	wikibaseList: {
		meta: { totalCount: number }
		data: Array<{ id: string; title: string; urls: { baseUrl: string; scriptPath: string | null } }>
	}
}

export type WbItemFragment = {
	id: string
	title: string
	urls: { baseUrl: string; scriptPath: string | null }
}

export type PageWikibasesQueryVariables = Exact<{
	pageNumber: number
	pageSize: number
	sortBy?: WikibaseSortInput | null | undefined
	wikibaseFilter?: WikibaseFilterInput | null | undefined
}>

export type PageWikibasesQuery = {
	wikibaseList: {
		meta: { totalCount: number; totalPages: number }
		data: Array<{
			id: string
			title: string
			category: WikibaseCategory | null
			description: string | null
			wikibaseType: WikibaseType
			urls: { baseUrl: string }
			quantityObservations: { mostRecent: { totalTriples: number | null } | null }
			recentChangesObservations: {
				mostRecent: { botChangeCount: number | null; humanChangeCount: number | null } | null
			}
		}>
	}
}

export type WbFragment = {
	id: string
	title: string
	category: WikibaseCategory | null
	description: string | null
	wikibaseType: WikibaseType
	urls: { baseUrl: string }
	quantityObservations: { mostRecent: { totalTriples: number | null } | null }
	recentChangesObservations: {
		mostRecent: { botChangeCount: number | null; humanChangeCount: number | null } | null
	}
}

export type TotalWikibasesQueryVariables = Exact<{ [key: string]: never }>

export type TotalWikibasesQuery = {
	wikibaseList: { meta: { totalCount: number } }
	aggregateQuantity: { totalTriples: number }
	aggregateRecentChanges: { botChangeCount: number; humanChangeCount: number }
}
