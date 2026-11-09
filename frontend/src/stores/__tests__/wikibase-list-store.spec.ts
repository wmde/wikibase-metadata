import { type ListWikibasesQuery } from '@/graphql/types'
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
		error: { value: false }
	})
}))

describe('useWikiListStore', async () => {
	beforeEach(() => {
		vi.resetAllMocks()
		setActivePinia(createPinia())
	})

	it('reflects query results', async () => {
		const results: ListWikibasesQuery = { wikibaseList: { meta: { totalCount: 0 }, data: [] } }
		mockOnResult.mockImplementationOnce((fn) => fn({ data: results }))
		const store = useWikiListStore()

		expect(store.wikibaseList).toEqual({
			data: { data: [], meta: { totalCount: 0 } },
			errorState: false,
			loading: false
		})
	})

	it('calls load on fetchWikibaseList', async () => {
		const results: ListWikibasesQuery = { wikibaseList: { meta: { totalCount: 0 }, data: [] } }
		mockOnResult.mockImplementationOnce((fn) => fn({ data: results }))
		const store = useWikiListStore()

		expect(mockLoad).toHaveBeenCalledTimes(0)
		store.fetchWikibaseList()
		expect(mockLoad).toHaveBeenCalledTimes(1)
	})
})
