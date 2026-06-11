import WikibaseSearch from '@/component/wikibase-table/WikibaseSearch.vue'
import vuetify from '@/plugin/vuetify'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

function sleep(milliseconds: number) {
	return new Promise((resolve) => {
		setTimeout(resolve, milliseconds)
	})
}

const mockSearchWikibaseText = vi.fn().mockName('searchWikibaseText')

vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiStore: (): WikibasePageStoreType => ({
		...mockWikiStore,
		searchWikibaseText: mockSearchWikibaseText
	})
}))

describe('WikibaseSearch', async () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.resetAllMocks()
	})

	it('renders  properly', async () => {
		const wrapper = mount(WikibaseSearch, { global: { plugins: [vuetify] } })

		const container = wrapper.find('.search-container')
		expect(container.exists()).toEqual(true)

		const searchContainer = container.find('.search-text')
		expect(searchContainer.exists()).toEqual(true)

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

		const wrapper = mount(WikibaseSearch, { global: { plugins: [vuetify] } })

		const container = wrapper.find('.search-container')
		expect(container.exists()).toEqual(true)

		const searchContainer = container.find('.search-text')
		expect(searchContainer.exists()).toEqual(true)

		const textField = searchContainer.find('.v-text-field')
		expect(textField.exists()).toEqual(true)

		const input = textField.find('input')
		expect(input.exists()).toEqual(true)

		await input.trigger('click')
		await nextTick()

		await input.setValue('ASDF')
		await nextTick()

		await sleep(300)

		expect(mockSearchWikibaseText).toHaveBeenCalledTimes(1)
		expect(mockSearchWikibaseText).lastCalledWith('ASDF')
	})

	it('raises error on non-allowed characters', async () => {
		const wrapper = mount(WikibaseSearch, { global: { plugins: [vuetify] } })

		const container = wrapper.find('.search-container')
		expect(container.exists()).toEqual(true)

		const searchContainer = container.find('.search-text')
		expect(searchContainer.exists()).toEqual(true)

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
		const wrapper = mount(WikibaseSearch, { global: { plugins: [vuetify] } })

		const container = wrapper.find('.search-container')
		expect(container.exists()).toEqual(true)

		const searchContainer = container.find('.search-text')
		expect(searchContainer.exists()).toEqual(true)

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

		expect(error.find('div').text()).toEqual('No results for "ASDF" — try a different keyword or category')
	})
})
