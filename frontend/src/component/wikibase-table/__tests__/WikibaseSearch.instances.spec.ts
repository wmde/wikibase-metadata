import WikibaseSearch from '@/component/wikibase-table/WikibaseSearch.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

const mockSearchWikibaseText = vi.fn().mockName('searchWikibaseText')
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
				menuValue: 'instances',
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
		expect(menuButton.text()).toEqual('Instances')

		const textField = searchContainer.find('.v-text-field')
		expect(textField.exists()).toEqual(true)

		const input = textField.find('input')
		expect(input.exists()).toEqual(true)

		const searchIcon = textField.find('.v-icon')
		expect(searchIcon.exists()).toEqual(true)

		const searchLabel = textField.find('.v-label')
		expect(searchLabel.exists()).toEqual(true)
		expect(searchLabel.text()).toEqual('Search Wikibase instances...')

		const error = container.find('.v-label.search-error')
		expect(error.exists()).toEqual(true)
	})

	it('triggers searchWikibaseText', async () => {
		expect(mockSearchWikibaseText).toHaveBeenCalledTimes(0)

		const wrapper = mount(WikibaseSearch, {
			global: { plugins: [vuetify] },
			props: {
				menuValue: 'instances',
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
		expect(menuButton.text()).toEqual('Instances')

		const textField = searchContainer.find('.v-text-field')
		expect(textField.exists()).toEqual(true)

		const input = textField.find('input')
		expect(input.exists()).toEqual(true)

		expect(mockSetSearchValue).toHaveBeenCalledTimes(0)

		await input.trigger('click')
		await nextTick()

		await input.setValue('ASDF')
		await nextTick()

		expect(mockSetSearchValue).toHaveBeenCalledTimes(1)
		expect(mockSetSearchValue).lastCalledWith('ASDF')
	})

	it('raises error on non-allowed characters', async () => {
		const wrapper = mount(WikibaseSearch, {
			global: { plugins: [vuetify] },
			props: {
				menuValue: 'instances',
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
		expect(menuButton.text()).toEqual('Instances')

		const textField = searchContainer.find('.v-text-field')
		expect(textField.exists()).toEqual(true)

		const input = textField.find('input')
		expect(input.exists()).toEqual(true)

		await input.trigger('click')
		await nextTick()

		await input.setValue('A$DF')
		await nextTick()

		const error = container.find('.v-label.search-error')
		expect(error.exists()).toEqual(true)

		expect(error.find('div').text()).toEqual('Disallowed Characters')
	})

	it('raises error on no results returned', async () => {
		const wrapper = mount(WikibaseSearch, {
			global: { plugins: [vuetify] },
			props: {
				menuValue: 'instances',
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
		expect(menuButton.text()).toEqual('Instances')

		const textField = searchContainer.find('.v-text-field')
		expect(textField.exists()).toEqual(true)

		const input = textField.find('input')
		expect(input.exists()).toEqual(true)

		await input.trigger('click')
		await nextTick()

		await input.setValue('ASDF')
		await nextTick()

		const error = container.find('.v-label.search-error')
		expect(error.exists()).toEqual(true)

		expect(error.find('div').text()).toEqual(
			'No results for "ASDF" — try a different keyword or category'
		)
	})
})
