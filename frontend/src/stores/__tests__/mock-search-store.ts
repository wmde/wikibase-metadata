import type { SearchStoreType } from '@/stores/search-store'
import { vi } from 'vitest'

const mockSearchStore: SearchStoreType = {
	menuValue: 'instances',
	setMenuValue: vi.fn().mockName('setMenuValue'),
	searchValue: '',
	debouncedSearchValue: '',
	setSearchValue: vi.fn().mockName('setSearchValue'),
	overrideDebounce: vi.fn().mockName('overrideDebounce')
}

export default mockSearchStore
