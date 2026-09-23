import WikibaseSearch from '@/component/wikibase-table/WikibaseSearch.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const mockSetMenuValue = vi.fn().mockName('setMenuValue')
const mockSetSearchValue = vi.fn().mockName('setSearchValue')

describe('WikibaseSearch', async () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.resetAllMocks()
	})

	it('renders properly', async () => {
		const wrapper = mount(WikibaseSearch, {
			global: { plugins: [vuetify] },
			props: {
				menuValue: 'items',
				setMenuValue: mockSetMenuValue,
				setSearchValue: mockSetSearchValue
			}
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
