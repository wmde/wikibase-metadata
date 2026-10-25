import WikibaseItemList from '@/component/wikibase-item-list/WikibaseItemList.vue'
import vuetify from '@/plugin/vuetify'
import mockSearchStore from '@/stores/__tests__/mock-search-store'
import mockWikiListStore from '@/stores/__tests__/mock-wikibase-list-store'
import type { SearchStoreType } from '@/stores/search-store'
import type { WikibaseListStoreType } from '@/stores/wikibase-list-store'
import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const { mockFetchWikibaseList, mockLoading } = vi.hoisted(() => ({
	mockFetchWikibaseList: vi.fn().mockName('fetchWikibaseList'),
	mockLoading: vi.fn()
}))

vi.mock('@/stores/wikibase-list-store', () => ({
	useWikiListStore: (): WikibaseListStoreType => ({
		...mockWikiListStore,
		fetchWikibaseList: mockFetchWikibaseList,
		wikibaseList: {
			...mockWikiListStore.wikibaseList,
			data: {
				meta: { totalCount: 5 },
				data: Array(5)
					.fill(0)
					.map((_, idx) => ({
						id: `${idx}`,
						title: `Wikibase ${idx}`,
						urls: { baseUrl: `https://test-wiki-${idx}.test`, scriptPath: 's' }
					}))
			},
			loading: mockLoading()
		}
	})
}))
vi.mock('@/stores/search-store', () => ({ useSearchStore: (): SearchStoreType => mockSearchStore }))

describe('WikibaseItemList', async () => {
	beforeEach(() => vi.resetAllMocks())

	it(`renders data properly`, async () => {
		mockLoading.mockReturnValueOnce(false)

		const wrapper = mount(WikibaseItemList, { global: { plugins: [vuetify] } })

		const container = wrapper.find('div.wikibase-item-list-container')
		expect(container.exists()).toEqual(true)
		expect(container.findAll('div.wikibase-item')).toHaveLength(5)

		expect(mockFetchWikibaseList).toHaveBeenCalledTimes(1)
	})

	it(`renders loading properly`, async () => {
		mockLoading.mockReturnValueOnce(true)

		const wrapper = mount(WikibaseItemList, { global: { plugins: [vuetify] } })

		expect(wrapper.text()).toEqual('Loading')
	})
})
