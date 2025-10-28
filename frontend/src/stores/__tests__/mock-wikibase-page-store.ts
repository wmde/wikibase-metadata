import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { vi } from 'vitest'

const mockWikiStore: WikibasePageStoreType = {
	fetchWikibasePage: vi.fn().mockName('fetchWikibasePage'),
	wikibasePage: { data: undefined, errorState: false, loading: false },
	pageNumber: 1,
	// setPageNumber: vi.fn().mockName('setPageNumber'),
	pageSize: 1,
	// setPageSize: vi.fn().mockName('setPageSize'),
	wikibaseFilter: {},
	excludeWikibaseTypes: vi.fn().mockName('excludeWikibaseTypes')
}

export default mockWikiStore
