import { SortColumn, SortDirection, WikibaseType, type PageWikibasesQuery } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

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

describe('useWikiStore', async () => {
	beforeEach(() => {
		vi.resetAllMocks()
		setActivePinia(createPinia())
	})

	it('reflects query results', async () => {
		const results: PageWikibasesQuery = {
			wikibaseList: { meta: { totalCount: 0, totalPages: 0 }, data: [] },
			aggregateQuantity: { totalTriples: 0 },
			aggregateRecentChanges: { botChangeCount: 0, humanChangeCount: 0 }
		}
		mockOnResult.mockImplementationOnce((fn) => fn({ data: results }))
		const store = useWikiStore()

		expect(store.pageNumber).toEqual(1)
		expect(store.pageSize).toEqual(25)
		expect(store.wikibaseFilter).toEqual({
			wikibaseType: { include: [WikibaseType.Cloud, WikibaseType.Suite, WikibaseType.Unknown] }
		})
		expect(store.wikibasePage).toEqual({
			data: { data: [], meta: { totalCount: 0, totalPages: 0, totalEdits: 0, totalTriples: 0 } },
			errorState: false,
			loading: false
		})
	})

	it('calls load on fetchWikibasePage', async () => {
		const results: PageWikibasesQuery = {
			wikibaseList: { meta: { totalCount: 0, totalPages: 0 }, data: [] },
			aggregateQuantity: { totalTriples: 0 },
			aggregateRecentChanges: { botChangeCount: 0, humanChangeCount: 0 }
		}
		mockOnResult.mockImplementationOnce((fn) => fn({ data: results }))
		const store = useWikiStore()

		expect(mockLoad).toHaveBeenCalledTimes(0)
		store.fetchWikibasePage()
		expect(mockLoad).toHaveBeenCalledTimes(1)
	})

	it('calls load on includeWikibaseTypes', async () => {
		const results: PageWikibasesQuery = {
			wikibaseList: { meta: { totalCount: 0, totalPages: 0 }, data: [] },
			aggregateQuantity: { totalTriples: 0 },
			aggregateRecentChanges: { botChangeCount: 0, humanChangeCount: 0 }
		}
		mockOnResult.mockImplementationOnce((fn) => fn({ data: results }))
		const store = useWikiStore()

		expect(mockLoad).toHaveBeenCalledTimes(0)

		store.includeWikibaseTypes([WikibaseType.Cloud])
		await nextTick()
		expect(mockLoad).toHaveBeenCalledTimes(1)
	})

	it('calls load on setPageNumber', async () => {
		const results: PageWikibasesQuery = {
			wikibaseList: { meta: { totalCount: 0, totalPages: 0 }, data: [] },
			aggregateQuantity: { totalTriples: 0 },
			aggregateRecentChanges: { botChangeCount: 0, humanChangeCount: 0 }
		}
		mockOnResult.mockImplementationOnce((fn) => fn({ data: results }))
		const store = useWikiStore()

		expect(mockLoad).toHaveBeenCalledTimes(0)

		store.setPageNumber(2)
		await nextTick()
		expect(mockLoad).toHaveBeenCalledTimes(1)
	})

	it('calls load on setPageSize', async () => {
		const results: PageWikibasesQuery = {
			wikibaseList: { meta: { totalCount: 0, totalPages: 0 }, data: [] },
			aggregateQuantity: { totalTriples: 0 },
			aggregateRecentChanges: { botChangeCount: 0, humanChangeCount: 0 }
		}
		mockOnResult.mockImplementationOnce((fn) => fn({ data: results }))
		const store = useWikiStore()

		expect(mockLoad).toHaveBeenCalledTimes(0)

		store.setPageSize(50)
		await nextTick()
		expect(mockLoad).toHaveBeenCalledTimes(1)
	})

	it('calls load on setSort', async () => {
		const results: PageWikibasesQuery = {
			wikibaseList: { meta: { totalCount: 0, totalPages: 0 }, data: [] },
			aggregateQuantity: { totalTriples: 0 },
			aggregateRecentChanges: { botChangeCount: 0, humanChangeCount: 0 }
		}
		mockOnResult.mockImplementationOnce((fn) => fn({ data: results }))
		const store = useWikiStore()

		expect(mockLoad).toHaveBeenCalledTimes(0)

		store.setSort({ column: SortColumn.Category, dir: SortDirection.Asc })
		await nextTick()
		expect(mockLoad).toHaveBeenCalledTimes(1)
	})
})
