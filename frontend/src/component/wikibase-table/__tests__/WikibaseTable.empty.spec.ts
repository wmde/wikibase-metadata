import { ResizeObserverMock } from '@/__tests__/global-mocks'
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import vuetify from '@/plugin/vuetify'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiStore: (): WikibasePageStoreType => mockWikiStore
}))

describe('WikibaseTable', async () => {
	it('renders header properly', async () => {
		const wrapper = mount(WikibaseTable, { global: { plugins: [vuetify] } })

		const tableContainer = wrapper.find('div.wikibase-table')
		expect(tableContainer.exists()).toEqual(true)

		const table = tableContainer.find('table')
		expect(table.exists()).toEqual(true)

		const tableHead = table.find('thead')
		expect(tableHead.exists()).toEqual(true)

		expect(tableHead.findAll('th').length).toEqual(8)

		expect(tableHead.findAll('th')[0]?.classes()).not.toContain('v-data-table__th--sortable')
		expect(tableHead.findAll('th')[0]?.find('i.v-icon').exists()).toEqual(false)
		expect(tableHead.findAll('th')[0]?.text()).toEqual('')

		expect(tableHead.findAll('th')[1]?.classes()).toContain('v-data-table__th--sortable')
		expect(tableHead.findAll('th')[1]?.find('i.v-icon').exists()).toEqual(true)
		expect(tableHead.findAll('th')[1]?.text()).toEqual('Type')

		expect(tableHead.findAll('th')[2]?.classes()).toContain('v-data-table__th--sortable')
		expect(tableHead.findAll('th')[2]?.find('i.v-icon').exists()).toEqual(true)
		expect(tableHead.findAll('th')[2]?.text()).toEqual('Title')

		expect(tableHead.findAll('th')[3]?.classes()).toContain('v-data-table__th--sortable')
		expect(tableHead.findAll('th')[3]?.find('i.v-icon').exists()).toEqual(true)
		expect(tableHead.findAll('th')[3]?.text()).toEqual('Triples')

		expect(tableHead.findAll('th')[4]?.classes()).toContain('v-data-table__th--sortable')
		expect(tableHead.findAll('th')[4]?.find('i.v-icon').exists()).toEqual(true)
		expect(tableHead.findAll('th')[4]?.text()).toEqual('Edits (last 30 days)')

		expect(tableHead.findAll('th')[5]?.classes()).toContain('v-data-table__th--sortable')
		expect(tableHead.findAll('th')[5]?.find('i.v-icon').exists()).toEqual(true)
		expect(tableHead.findAll('th')[5]?.text()).toEqual('Category')

		expect(tableHead.findAll('th')[6]?.classes()).not.toContain('v-data-table__th--sortable')
		expect(tableHead.findAll('th')[6]?.find('i.v-icon').exists()).toEqual(false)
		expect(tableHead.findAll('th')[6]?.text()).toEqual('Description')

		expect(tableHead.findAll('th')[7]?.classes()).not.toContain('v-data-table__th--sortable')
		expect(tableHead.findAll('th')[7]?.find('i.v-icon').exists()).toEqual(false)
		expect(tableHead.findAll('th')[7]?.text()).toEqual('Details')
	})

	it('renders empty properly', async () => {
		const wrapper = mount(WikibaseTable, { global: { plugins: [vuetify] } })

		const tableContainer = wrapper.find('div.wikibase-table')
		expect(tableContainer.exists()).toEqual(true)

		const table = tableContainer.find('table')
		expect(table.exists()).toEqual(true)

		expect(table.find('tbody').findAll('tr').length).toEqual(1)

		const loadingRow = table.find('tbody').find('tr.v-data-table-rows-loading')
		expect(loadingRow.exists()).toEqual(false)

		const noDataRow = table.find('tbody').find('tr.v-data-table-rows-no-data')
		expect(noDataRow.exists()).toEqual(true)
		expect(noDataRow.text()).toEqual('No data available')

		expect(tableContainer.find('hr.v-divider').exists()).toEqual(true)

		const footerContainer = tableContainer.find('div.v-data-table-footer')
		expect(footerContainer.exists()).toEqual(true)

		const itemsPerPageContainer = footerContainer.find('div.v-data-table-footer__items-per-page')
		expect(itemsPerPageContainer.exists()).toEqual(true)

		const infoContainer = footerContainer.find('div.v-data-table-footer__info')
		expect(infoContainer.exists()).toEqual(true)
		expect(infoContainer.text()).toEqual('0-0 of 0')

		const paginationContainer = footerContainer.find('div.v-data-table-footer__pagination')
		expect(paginationContainer.exists()).toEqual(true)
	})
})
