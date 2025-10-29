import { WikibaseType } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

const { mockLoad, mockUseLazyQuery } = vi.hoisted(() => ({
	mockLoad: vi.fn().mockName('load'),
	mockUseLazyQuery: vi.fn().mockName('useLazyQuery')
}))

vi.mock('@vue/apollo-composable', () => ({
	provideApolloClient: vi.fn().mockName('provideApolloClient'),
	useLazyQuery: mockUseLazyQuery.mockReturnValueOnce({
		load: mockLoad,
		result: { value: { wikibaseList: { meta: { totalCount: 0 }, data: [] } } },
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
		const store = useWikiStore()

		expect(store.pageNumber).toEqual(1)
		expect(store.pageSize).toEqual(10000)
		expect(store.wikibaseFilter).toEqual({
			wikibaseType: { include: [WikibaseType.Cloud, WikibaseType.Suite, WikibaseType.Unknown] }
		})
		expect(store.wikibasePage).toEqual({
			data: { wikibaseList: { data: [], meta: { totalCount: 0 } } },
			errorState: false,
			loading: false
		})
	})

	it('calls load on fetchWikibasePage', async () => {
		const store = useWikiStore()

		expect(mockLoad).toHaveBeenCalledTimes(0)
		store.fetchWikibasePage()
		expect(mockLoad).toHaveBeenCalledTimes(1)
	})

	it('calls load on includeWikibaseTypes', async () => {
		const store = useWikiStore()

		expect(mockLoad).toHaveBeenCalledTimes(0)

		store.includeWikibaseTypes([WikibaseType.Cloud])
		await nextTick()
		expect(mockLoad).toHaveBeenCalledTimes(1)
	})
})
