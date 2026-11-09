import type { WikibaseTotalStoreType } from '@/stores/wikibase-total-store'
import { vi } from 'vitest'

const mockWikiTotalStore: WikibaseTotalStoreType = {
	fetchWikibaseTotal: vi.fn().mockName('fetchWikibaseTotal'),
	wikibaseTotal: { data: undefined, errorState: false, loading: false }
}

export default mockWikiTotalStore
