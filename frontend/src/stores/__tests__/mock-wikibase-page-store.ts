import { SortColumn, SortDirection } from '@/graphql/types'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { vi } from 'vitest'

const mockWikiStore: WikibasePageStoreType = {
	fetchWikibasePage: vi.fn().mockName('fetchWikibasePage'),
	wikibasePage: { data: undefined, errorState: false, loading: false },
	pageNumber: 1,
	setPageNumber: vi.fn().mockName('setPageNumber'),
	pageSize: 1,
	setPageSize: vi.fn().mockName('setPageSize'),
	sortBy: { column: SortColumn.Triples, dir: SortDirection.Desc },
	setSort: vi.fn().mockName('sortByColumn'),
	wikibaseFilter: {},
	includeWikibaseTypes: vi.fn().mockName('includeWikibaseTypes')
}

export default mockWikiStore
