import type { WikibaseListStoreType } from '@/stores/wikibase-list-store'
import { vi } from 'vitest'

const mockWikiListStore: WikibaseListStoreType = {
	fetchWikibaseList: vi.fn().mockName('fetchWikibaseList'),
	wikibaseList: { data: undefined, errorState: false, loading: false }
}

export default mockWikiListStore
