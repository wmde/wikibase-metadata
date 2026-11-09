import { type TotalWikibasesQuery } from '@/graphql/types'
import { useWikiTotalStore } from '@/stores/wikibase-total-store'
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
		error: { value: false }
	})
}))

describe('useWikiTotalStore', async () => {
	beforeEach(() => {
		vi.resetAllMocks()
		setActivePinia(createPinia())
	})

	it('reflects query results', async () => {
		const results: TotalWikibasesQuery = {
			wikibaseList: { meta: { totalCount: 0 } },
			aggregateQuantity: { totalTriples: 0 },
			aggregateRecentChanges: { botChangeCount: 0, humanChangeCount: 0 }
		}
		mockOnResult.mockImplementationOnce((fn) => fn({ data: results }))
		const store = useWikiTotalStore()

		expect(store.wikibaseTotal).toEqual({
			data: { totalCount: 0, totalEdits: 0, totalTriples: 0 },
			errorState: false,
			loading: false
		})
	})

	it('calls load on fetchWikibaseTotal', async () => {
		const results: TotalWikibasesQuery = {
			wikibaseList: { meta: { totalCount: 0 } },
			aggregateQuantity: { totalTriples: 0 },
			aggregateRecentChanges: { botChangeCount: 0, humanChangeCount: 0 }
		}
		mockOnResult.mockImplementationOnce((fn) => fn({ data: results }))
		const store = useWikiTotalStore()

		expect(mockLoad).toHaveBeenCalledTimes(0)
		store.fetchWikibaseTotal()
		expect(mockLoad).toHaveBeenCalledTimes(1)
	})
})
