import { ResizeObserverMock } from '@/__tests__/global-mocks'
import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import vuetify from '@/plugin/vuetify'
import mockMenuStore from '@/stores/__tests__/mock-menu-store'
import mockWikiListStore from '@/stores/__tests__/mock-wikibase-list-store'
import mockWikiPageStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { MenuStoreType } from '@/stores/menu-store'
import type { WikibaseListStoreType } from '@/stores/wikibase-list-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

const { mockMenuValue } = vi.hoisted(() => ({ mockMenuValue: vi.fn().mockName('') }))

vi.mock('@/stores/menu-store', () => ({
	useMenuStore: (): MenuStoreType => ({ ...mockMenuStore, value: mockMenuValue() })
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
	useWikiPageStore: (): WikibasePageStoreType => mockWikiPageStore
}))

describe('WikibaseTableContainer', async () => {
	it('renders instances properly', async () => {
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
})
