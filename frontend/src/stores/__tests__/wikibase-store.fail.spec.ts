import { useSingleWikiStore } from '@/stores/wikibase-store'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const { mockLoad, mockUseLazyQuery } = vi.hoisted(() => ({
	mockLoad: vi.fn().mockName('load'),
	mockUseLazyQuery: vi.fn().mockName('useLazyQuery')
}))

vi.mock('@vue/apollo-composable', () => ({
	provideApolloClient: vi.fn().mockName('provideApolloClient'),
	useLazyQuery: mockUseLazyQuery.mockReturnValueOnce({
		load: mockLoad,
		result: {
			value: undefined
		},
		loading: { value: false },
		error: { value: true }
	})
}))

describe('useSingleWikiStore', async () => {
	beforeEach(() => {
		vi.resetAllMocks()
		setActivePinia(createPinia())
	})

	it('reflects query error', async () => {
		const store = useSingleWikiStore()

		expect(store.wikibase).toEqual({
			data: null,
			errorState: true,
			loading: false
		})
	})
})
