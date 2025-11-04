import { WikibaseType } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
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

describe('useWikiStore', async () => {
	beforeEach(() => {
		vi.resetAllMocks()
		setActivePinia(createPinia())
	})

	it('reflects query failure', async () => {
		const store = useWikiStore()

		expect(store.pageNumber).toEqual(1)
		expect(store.pageSize).toEqual(10)
		expect(store.wikibaseFilter).toEqual({
			wikibaseType: { include: [WikibaseType.Cloud, WikibaseType.Suite, WikibaseType.Unknown] }
		})
		expect(store.wikibasePage).toEqual({
			data: undefined,
			errorState: true,
			loading: false
		})
	})
})
