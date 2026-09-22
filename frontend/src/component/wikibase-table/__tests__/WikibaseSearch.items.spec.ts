import WikibaseSearch from '@/component/wikibase-table/WikibaseSearch.vue'
import vuetify from '@/plugin/vuetify'
import mockWikiPageStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const mockSearchWikibaseText = vi.fn().mockName('searchWikibaseText')
const mockSetMenuValue = vi.fn().mockName('setMenuValue')

vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiPageStore: (): WikibasePageStoreType => ({
		...mockWikiPageStore,
		searchWikibaseText: mockSearchWikibaseText
	})
}))

describe('WikibaseSearch', async () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.resetAllMocks()
	})

	it('renders properly', async () => {
		const wrapper = mount(WikibaseSearch, {
			global: { plugins: [vuetify] },
			props: { menuValue: 'items', setMenuValue: mockSetMenuValue }
		})

		const container = wrapper.find('.search-container')
		expect(container.exists()).toEqual(true)

		const searchContainer = container.find('.search-text')
		expect(searchContainer.exists()).toEqual(true)

		const menuButton = searchContainer.find('.v-btn')
		expect(menuButton.exists()).toEqual(true)
		expect(menuButton.text()).toEqual('Items')
	})

})
