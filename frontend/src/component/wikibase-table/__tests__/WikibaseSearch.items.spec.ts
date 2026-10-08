import WikibaseSearch from '@/component/wikibase-table/WikibaseSearch.vue'
import vuetify from '@/plugin/vuetify'
import mockMenuStore from '@/stores/__tests__/mock-menu-store'
import type { MenuStoreType } from '@/stores/menu-store'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/stores/menu-store', () => ({
	useMenuStore: (): MenuStoreType => ({ ...mockMenuStore, value: 'items' })
}))

const mockSetSearchValue = vi.fn().mockName('setSearchValue')

describe('WikibaseSearch', async () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.resetAllMocks()
	})

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
