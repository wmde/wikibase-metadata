import { ResizeObserverMock } from '@/__tests__/global-mocks'
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import vuetify from '@/plugin/vuetify'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiStore: (): WikibasePageStoreType => ({
		...mockWikiStore,
		wikibasePage: { ...mockWikiStore.wikibasePage, loading: true }
	})
}))

describe('WikibaseTable', async () => {
	it('renders loading properly', async () => {
		const wrapper = mount(WikibaseTable, { global: { plugins: [vuetify] } })

		const tableContainer = wrapper.find('div.wikibase-table')
		expect(tableContainer.exists()).toEqual(true)
		expect(tableContainer.classes()).toContain('v-table')
		expect(tableContainer.classes()).toContain('v-table--striped-even')
		expect(tableContainer.classes()).toContain('v-data-table')
		expect(tableContainer.classes()).toContain('v-data-table--loading')

		const table = tableContainer.find('table')
		expect(table.exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr').length).toEqual(1)

		const loadingRow = table.find('tbody').find('tr.v-data-table-rows-loading')
		expect(loadingRow.exists()).toEqual(true)
		expect(loadingRow.find('td').text()).toContain('Loading items...')

		const noDataRow = table.find('tbody').find('tr.v-data-table-rows-no-data')
		expect(noDataRow.exists()).toEqual(false)
	})
})
