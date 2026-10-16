import type { SearchStoreType } from '@/stores/search-store'
import { vi } from 'vitest'

const mockSearchStore: SearchStoreType = {
	menuValue: 'instances',
	setMenuValue: vi.fn().mockName('setValue')
}

export default mockSearchStore
