import WikibaseSearch from '@/component/wikibase-table/WikibaseSearch.vue'
import vuetify from '@/plugin/vuetify'
import mockSearchStore from '@/stores/__tests__/mock-search-store'
import mockWikiPageStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { SearchStoreType } from '@/stores/search-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

const { mockMenuValue, mockSearchValue, mockSetSearchValue } = vi.hoisted(() => ({
	mockMenuValue: vi.fn().mockName('menuValue'),
	mockSearchValue: vi.fn().mockName('searchValue'),
	mockSetSearchValue: vi.fn().mockName('setSearchValue')
}))
vi.mock('@/stores/search-store', () => ({
	useSearchStore: (): SearchStoreType => ({
		...mockSearchStore,
		menuValue: mockMenuValue(),
		searchValue: mockSearchValue(),
		setSearchValue: mockSetSearchValue
	})
}))
vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiPageStore: (): WikibasePageStoreType => mockWikiPageStore
}))

describe('WikibaseSearch', async () => {
	describe('search instances', async () => {
		beforeEach(() => {
			vi.resetAllMocks()
			mockMenuValue.mockReturnValueOnce('instances')
		})

		it('renders properly', async () => {
			mockSearchValue.mockReturnValueOnce('')

			const wrapper = mount(WikibaseSearch, { global: { plugins: [vuetify] } })

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

		it('triggers setSearchValue', async () => {
			mockSearchValue.mockReturnValueOnce('')

			const wrapper = mount(WikibaseSearch, { global: { plugins: [vuetify] } })

			const container = wrapper.find('.search-container')
			const searchContainer = container.find('.search-text')
			const textField = searchContainer.find('.v-text-field')
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
	})

	describe('search items', async () => {
		beforeEach(() => {
			vi.resetAllMocks()
			mockMenuValue.mockReturnValueOnce('items')
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

			const textField = searchContainer.find('.v-text-field')
			const searchLabel = textField.find('.v-label')
			expect(searchLabel.text()).toEqual('Search for items across all Wikibase instances...')
		})
	})
})
