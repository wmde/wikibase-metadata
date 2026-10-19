import WikibaseItemList from '@/component/wikibase-item-list/WikibaseItemList.vue'
import vuetify from '@/plugin/vuetify'
import mockWikiListStore from '@/stores/__tests__/mock-wikibase-list-store'
import type { WikibaseListStoreType } from '@/stores/wikibase-list-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

const { mockFetchWikibaseList } = vi.hoisted(() => ({
	mockFetchWikibaseList: vi.fn().mockName('fetchWikibaseList')
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
			}
		}
	})
}))

describe('WikibaseItemList', async () => {
	it(`renders data properly`, async () => {
		const wrapper = mount(WikibaseItemList, { global: { plugins: [vuetify] } })

		const container = wrapper.find('div.wikibase-item-list-container')
		expect(container.exists()).toEqual(true)
		expect(container.findAll('div.wikibase-item')).toHaveLength(5)

		expect(mockFetchWikibaseList).toHaveBeenCalledTimes(1)
	})
})
