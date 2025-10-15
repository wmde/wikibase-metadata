import { vi } from 'vitest'
import type { WikibaseStoreType } from '../wikibase-store'

const mockSingleWikiStore: WikibaseStoreType = {
	fetchWikibase: vi.fn().mockName('fetchWikibase'),
	wikibaseId: undefined,
	wikibase: { data: null, errorState: false, loading: false },
	searchWikibase: vi.fn().mockName('searchWikibase')
}

export default mockSingleWikiStore
