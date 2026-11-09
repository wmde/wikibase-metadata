import { ResizeObserverMock } from '@/__tests__/global-mocks'
import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import vuetify from '@/plugin/vuetify'
import mockSearchStore from '@/stores/__tests__/mock-search-store'
import mockWikiListStore from '@/stores/__tests__/mock-wikibase-list-store'
import mockWikiPageStore from '@/stores/__tests__/mock-wikibase-page-store'
import mockWikiTotalStore from '@/stores/__tests__/mock-wikibase-total-store'
import type { SearchStoreType } from '@/stores/search-store'
import type { WikibaseListStoreType } from '@/stores/wikibase-list-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import type { WikibaseTotalStoreType } from '@/stores/wikibase-total-store'
import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

const { mockErrorState, mockMenuValue } = vi.hoisted(() => ({
	mockMenuValue: vi.fn().mockName(''),
	mockErrorState: vi.fn().mockName('')
}))

vi.mock('@/stores/search-store', () => ({
	useSearchStore: (): SearchStoreType => ({ ...mockSearchStore, menuValue: mockMenuValue() }),
	SEARCH_PARAM_NAME: 'search'
}))
vi.mock('@/stores/wikibase-list-store', () => ({
	useWikiListStore: (): WikibaseListStoreType => ({
		...mockWikiListStore,
		wikibaseList: {
			loading: false,
			errorState: false,
			data: {
				meta: { totalCount: 1 },
				data: [
					{
						id: '2',
						title: 'Test Wikibase #2',
						urls: { baseUrl: 'test-wikibase-002.test', scriptPath: 'wiki' }
					}
				]
			}
		}
	})
}))
vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiPageStore: (): WikibasePageStoreType => ({
		...mockWikiPageStore,
		wikibasePage: { ...mockWikiPageStore.wikibasePage, errorState: mockErrorState() }
	})
}))
vi.mock('@/stores/wikibase-total-store', () => ({
	useWikiTotalStore: (): WikibaseTotalStoreType => mockWikiTotalStore
}))

describe('WikibaseTableContainer', async () => {
	beforeEach(() => {
		vi.resetAllMocks()
	})

	it('renders instances properly', async () => {
		mockErrorState.mockReturnValueOnce(false)
		mockMenuValue.mockReturnValueOnce('instances')

		const wrapper = mount(WikibaseTableContainer, { global: { plugins: [vuetify] } })

		const tableContainer = wrapper.find('div.wikibase-table-container')
		expect(tableContainer.exists()).toEqual(true)

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(false)

		const showing = wrapper.find('div.show-count')
		expect(showing.exists()).toEqual(false)

		const search = wrapper.find('div.search-text')
		expect(search.exists()).toEqual(true)

		const table = tableContainer.find('div.wikibase-table')
		expect(table.exists()).toEqual(true)

		const itemContainer = tableContainer.find('div.wikibase-item-list-container')
		expect(itemContainer.exists()).toEqual(false)
	})

	it('renders items properly', async () => {
		mockErrorState.mockReturnValueOnce(false)
		mockMenuValue.mockReturnValueOnce('items')

		const wrapper = mount(WikibaseTableContainer, { global: { plugins: [vuetify] } })

		const tableContainer = wrapper.find('div.wikibase-table-container')
		expect(tableContainer.exists()).toEqual(true)

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(false)

		const showing = wrapper.find('div.show-count')
		expect(showing.exists()).toEqual(false)

		const search = wrapper.find('div.search-text')
		expect(search.exists()).toEqual(true)

		const table = tableContainer.find('div.wikibase-table')
		expect(table.exists()).toEqual(false)

		const itemContainer = tableContainer.find('div.wikibase-item-list-container')
		expect(itemContainer.exists()).toEqual(true)
	})

	it('renders error properly', async () => {
		mockErrorState.mockReturnValueOnce(true)

		const wrapper = mount(WikibaseTableContainer, { global: { plugins: [vuetify] } })

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(true)
		expect(alert.classes()).toContain('text-error')

		const alertTitle = alert.find('div.v-alert-title')
		expect(alertTitle.exists()).toEqual(true)
		expect(alertTitle.text()).toEqual('Error')

		expect(alert.text()).toContain('Error fetching data')
	})
})
