import WikibaseSearch from '@/component/wikibase-table/WikibaseSearch.vue'
import vuetify from '@/plugin/vuetify'
import mockSearchStore from '@/stores/__tests__/mock-search-store'
import mockWikiPageStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { SearchStoreType } from '@/stores/search-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/stores/search-store', () => ({
	useSearchStore: (): SearchStoreType => ({ ...mockSearchStore, menuValue: 'items' })
}))
vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiPageStore: (): WikibasePageStoreType => mockWikiPageStore
}))

const mockSetSearchValue = vi.fn().mockName('setSearchValue')

describe('WikibaseSearch', async () => {
	beforeEach(() => vi.resetAllMocks())

	it('renders properly', async () => {
		const wrapper = mount(WikibaseSearch, {
			global: { plugins: [vuetify] },
			props: { setSearchValue: mockSetSearchValue }
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
