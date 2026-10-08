import type { MenuStoreType } from '@/stores/menu-store'
import { vi } from 'vitest'

const mockMenuStore: MenuStoreType = {
	value: 'instances',
	setValue: vi.fn().mockName('setValue')
}

export default mockMenuStore
