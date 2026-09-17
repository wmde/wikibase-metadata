import { useWikiListStore } from '@/stores/wikibase-list-store'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const { mockLoad, mockOnResult, mockUseLazyQuery } = vi.hoisted(() => ({
	mockLoad: vi.fn().mockName('load'),
	mockOnResult: vi.fn().mockName('onResult'),
	mockUseLazyQuery: vi.fn().mockName('useLazyQuery')
}))

vi.mock('@vue/apollo-composable', () => ({
	provideApolloClient: vi.fn().mockName('provideApolloClient'),
	useLazyQuery: mockUseLazyQuery.mockReturnValueOnce({
		load: mockLoad,
		onResult: mockOnResult,
		loading: { value: false },
		error: { value: true }
	})
}))

describe('useWikiListStore', async () => {
	beforeEach(() => {
		vi.resetAllMocks()
		setActivePinia(createPinia())
	})

	it('reflects query failure', async () => {
		const store = useWikiListStore()

		expect(store.wikibaseList).toEqual({ data: undefined, errorState: true, loading: false })
	})
})
