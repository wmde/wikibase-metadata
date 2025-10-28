import type { WikibaseStoreType } from '@/stores/wikibase-store'
import { vi } from 'vitest'

const mockSingleWikiStore: WikibaseStoreType = {
	wikibaseId: undefined,
	wikibase: { data: null, errorState: false, loading: false },
	searchWikibase: vi.fn().mockName('searchWikibase')
}

export default mockSingleWikiStore
