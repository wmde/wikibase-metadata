import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { vi } from 'vitest'

const mockWikiPageStore: WikibasePageStoreType = {
	fetchWikibasePage: vi.fn().mockName('fetchWikibasePage'),
	wikibasePage: { data: undefined, errorState: false, loading: false },
	pageNumber: 1,
	setPageNumber: vi.fn().mockName('setPageNumber'),
	pageSize: 1,
	setPageSize: vi.fn().mockName('setPageSize'),
	sortBy: { column: 'TRIPLES', dir: 'DESC' },
	setSort: vi.fn().mockName('sortByColumn'),
	wikibaseFilter: {},
	searchWikibaseText: vi.fn().mockName('searchWikibaseText')
}

export default mockWikiPageStore
