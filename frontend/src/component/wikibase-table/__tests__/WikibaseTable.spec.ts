import { ResizeObserverMock } from '@/__tests__/global-mocks'
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import { WikibaseCategory, WikibaseType, type WbFragment } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

const testWikibasesAlt: WbFragment[] = [
	{
		id: '1',
		title: 'Test Wikibase',
		description: 'An Example for the Purposes of Testing',
		urls: { baseUrl: 'test-wikibase-001.test' },
		quantityObservations: {},
		recentChangesObservations: {},
		wikibaseType: WikibaseType.Cloud
	},
	{
		id: '2',
		title: 'Test Wikibase #2',
		category: WikibaseCategory.FictionalAndCreativeWorks,
		urls: { baseUrl: 'test-wikibase-002.test' },
		quantityObservations: { mostRecent: { totalTriples: 14 } },
		recentChangesObservations: {},
		wikibaseType: WikibaseType.Suite
	},
	{
		id: '3',
		title: 'Test Wikibase #3',
		urls: { baseUrl: 'test-wikibase-003.test' },
		quantityObservations: { mostRecent: { totalTriples: 1 } },
		recentChangesObservations: { mostRecent: { botChangeCount: 100 } },
		wikibaseType: WikibaseType.Other
	},
	{
		id: '4',
		title: 'Test Wikibase #4',
		category: WikibaseCategory.TechnologyAndOpenSource,
		urls: { baseUrl: 'test-wikibase-004.test' },
		quantityObservations: { mostRecent: {} },
		recentChangesObservations: { mostRecent: { humanChangeCount: 31 } },
		wikibaseType: WikibaseType.Suite
	},
	{
		id: '5',
		title: 'Test Wikibase #5',
		urls: { baseUrl: 'test-wikibase-005.test' },
		quantityObservations: { mostRecent: { totalTriples: 300 } },
		recentChangesObservations: { mostRecent: { humanChangeCount: 31, botChangeCount: 69 } },
		wikibaseType: WikibaseType.Unknown
	}
]
const manyTestWikibases: WbFragment[] = ''
	.padStart(1000, '0')
	.split('0')
	.map(
		(_, index): WbFragment => ({
			id: `${index}`,
			title: `Test Wikibase #${index}`,
			urls: { baseUrl: `https://test-wikibase-${index}.test` },
			quantityObservations: { mostRecent: index % 5 == 0 ? undefined : { totalTriples: index } },
			recentChangesObservations: {
				mostRecent:
					index % 7 == 0
						? undefined
						: {
								botChangeCount: index % 11 == 0 ? undefined : index,
								humanChangeCount: index % 13 == 0 ? undefined : index
							}
			},
			wikibaseType: WikibaseType.Unknown
		})
	)

describe('WikibaseTable', async () => {
	beforeEach(() => setActivePinia(createPinia()))

	it('renders header properly', async () => {
		const wrapper = mount(WikibaseTable, {
			global: { plugins: [vuetify] },
			props: { error: false, loading: false, wikibases: testWikibasesAlt.slice(0, 1) }
		})

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(false)

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
		expect(tableHead.findAll('th')[4]?.text()).toEqual('Edits')

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

	it('renders data properly', async () => {
		const wrapper = mount(WikibaseTable, {
			global: { plugins: [vuetify] },
			props: { error: false, loading: false, wikibases: testWikibasesAlt }
		})

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(false)

		const tableContainer = wrapper.find('div.wikibase-table')
		expect(tableContainer.exists()).toEqual(true)

		const table = tableContainer.find('table')
		expect(table.exists()).toEqual(true)

		expect(table.find('tbody').findAll('tr').length).toEqual(5)

		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[0]?.text())
		).toEqual(['1', '2', '3', '4', '5'])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[1]?.text())
		).toEqual(['UNKNOWN', 'SUITE', 'OTHER', 'CLOUD', 'SUITE'])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[2]?.text())
		).toEqual([
			'Test Wikibase #5',
			'Test Wikibase #2',
			'Test Wikibase #3',
			'Test Wikibase',
			'Test Wikibase #4'
		])
		table
			.find('tbody')
			.findAll('tr')
			.forEach((tr) => expect(tr.findAll('td')[2]?.find('a').exists()).toEqual(true))
		table
			.find('tbody')
			.findAll('tr')
			.forEach((tr) => expect(tr.findAll('td')[2]?.find('a').attributes()).toHaveProperty('href'))
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[2]?.find('a').attributes()['href'])
		).toEqual([
			'test-wikibase-005.test',
			'test-wikibase-002.test',
			'test-wikibase-003.test',
			'test-wikibase-001.test',
			'test-wikibase-004.test'
		])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[3]?.text())
		).toEqual(['300', '14', '1', '–', '–'])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[4]?.text())
		).toEqual(['100', '–', '100', '–', '31'])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[5]?.text())
		).toEqual(['', 'FICTIONAL_AND_CREATIVE_WORKS', '', '', 'TECHNOLOGY_AND_OPEN_SOURCE'])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[6]?.text())
		).toEqual(['', '', '', 'An Example for the Purposes of Testing', ''])

		const footerContainer = tableContainer.find('div.v-data-table-footer')
		expect(footerContainer.exists()).toEqual(true)

		const infoContainer = footerContainer.find('div.v-data-table-footer__info')
		expect(infoContainer.exists()).toEqual(true)
		expect(infoContainer.text()).toEqual('1-5 of 5')
	})

	it('changes page properly', async () => {
		const wrapper = mount(WikibaseTable, {
			global: { plugins: [vuetify] },
			props: { error: false, loading: false, wikibases: manyTestWikibases }
		})

		const tableContainer = wrapper.find('div.wikibase-table')
		expect(tableContainer.exists()).toEqual(true)

		const footerContainer = tableContainer.find('div.v-data-table-footer')
		expect(footerContainer.exists()).toEqual(true)

		const infoContainer = footerContainer.find('div.v-data-table-footer__info')
		expect(infoContainer.exists()).toEqual(true)
		expect(infoContainer.text()).toEqual('1-10 of 1001')

		const paginationContainer = footerContainer.find('div.v-data-table-footer__pagination')
		expect(paginationContainer.exists()).toEqual(true)
		expect(paginationContainer.findAll('button.v-btn').length).toEqual(4)
		expect(paginationContainer.findAll('button.v-btn')[0]?.classes()).toContain('v-btn--disabled')
		expect(paginationContainer.findAll('button.v-btn')[1]?.classes()).toContain('v-btn--disabled')
		expect(paginationContainer.findAll('button.v-btn')[2]?.classes()).not.toContain(
			'v-btn--disabled'
		)
		expect(paginationContainer.findAll('button.v-btn')[3]?.classes()).not.toContain(
			'v-btn--disabled'
		)

		await paginationContainer.findAll('button.v-btn')[2]?.trigger('click')
		await nextTick()

		expect(infoContainer.text()).toEqual('11-20 of 1001')
		expect(paginationContainer.findAll('button.v-btn')[0]?.classes()).not.toContain(
			'v-btn--disabled'
		)
		expect(paginationContainer.findAll('button.v-btn')[1]?.classes()).not.toContain(
			'v-btn--disabled'
		)
		expect(paginationContainer.findAll('button.v-btn')[2]?.classes()).not.toContain(
			'v-btn--disabled'
		)
		expect(paginationContainer.findAll('button.v-btn')[3]?.classes()).not.toContain(
			'v-btn--disabled'
		)

		await paginationContainer.findAll('button.v-btn')[3]?.trigger('click')
		await nextTick()

		expect(infoContainer.text()).toEqual('1001-1001 of 1001')
		expect(paginationContainer.findAll('button.v-btn')[0]?.classes()).not.toContain(
			'v-btn--disabled'
		)
		expect(paginationContainer.findAll('button.v-btn')[1]?.classes()).not.toContain(
			'v-btn--disabled'
		)
		expect(paginationContainer.findAll('button.v-btn')[2]?.classes()).toContain('v-btn--disabled')
		expect(paginationContainer.findAll('button.v-btn')[3]?.classes()).toContain('v-btn--disabled')
	})

	it('re-sorts data properly', async () => {
		const wrapper = mount(WikibaseTable, {
			global: { plugins: [vuetify] },
			props: { error: false, loading: false, wikibases: testWikibasesAlt }
		})

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(false)

		const tableContainer = wrapper.find('div.wikibase-table')
		expect(tableContainer.exists()).toEqual(true)

		const table = tableContainer.find('table')
		expect(table.exists()).toEqual(true)

		const tableHead = table.find('thead')
		expect(tableHead.exists()).toEqual(true)

		expect(tableHead.findAll('th').length).toEqual(8)

		expect(tableHead.findAll('th')[4]?.classes()).toContain('v-data-table__th--sortable')
		expect(tableHead.findAll('th')[4]?.find('i.v-icon').exists()).toEqual(true)
		expect(tableHead.findAll('th')[4]?.text()).toEqual('Edits')

		await tableHead.findAll('th')[4]?.trigger('click')
		await nextTick()

		expect(table.find('tbody').findAll('tr').length).toEqual(5)

		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[1]?.text())
		).toEqual(['CLOUD', 'SUITE', 'SUITE', 'OTHER', 'UNKNOWN'])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[2]?.text())
		).toEqual([
			'Test Wikibase',
			'Test Wikibase #2',
			'Test Wikibase #4',
			'Test Wikibase #3',
			'Test Wikibase #5'
		])
		table
			.find('tbody')
			.findAll('tr')
			.forEach((tr) => expect(tr.findAll('td')[2]?.find('a').exists()).toEqual(true))
		table
			.find('tbody')
			.findAll('tr')
			.forEach((tr) => expect(tr.findAll('td')[2]?.find('a').attributes()).toHaveProperty('href'))
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[2]?.find('a').attributes()['href'])
		).toEqual([
			'test-wikibase-001.test',
			'test-wikibase-002.test',
			'test-wikibase-004.test',
			'test-wikibase-003.test',
			'test-wikibase-005.test'
		])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[3]?.text())
		).toEqual(['–', '14', '–', '1', '300'])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[4]?.text())
		).toEqual(['–', '–', '31', '100', '100'])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[5]?.text())
		).toEqual(['', 'FICTIONAL_AND_CREATIVE_WORKS', 'TECHNOLOGY_AND_OPEN_SOURCE', '', ''])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[6]?.text())
		).toEqual(['An Example for the Purposes of Testing', '', '', '', ''])
	})

	it('renders empty properly', async () => {
		const wrapper = mount(WikibaseTable, {
			global: { plugins: [vuetify] },
			props: { error: false, loading: false, wikibases: undefined }
		})

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(false)

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

	it('renders error properly', async () => {
		const wrapper = mount(WikibaseTable, {
			global: { plugins: [vuetify] },
			props: { error: true, loading: false, wikibases: undefined }
		})

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(true)
		expect(alert.classes()).toContain('text-error')

		const alertTitle = alert.find('div.v-alert-title')
		expect(alertTitle.exists()).toEqual(true)
		expect(alertTitle.text()).toEqual('Error')

		expect(alert.text()).toContain('Error fetching data')

		const tableContainer = wrapper.find('div.wikibase-table')
		expect(tableContainer.exists()).toEqual(true)

		const table = tableContainer.find('table')
		expect(table.exists()).toEqual(true)

		const loadingRow = table.find('tbody').find('tr.v-data-table-rows-loading')
		expect(loadingRow.exists()).toEqual(false)
	})

	it('renders loading properly', async () => {
		const wrapper = mount(WikibaseTable, {
			global: { plugins: [vuetify] },
			props: { error: false, loading: true, wikibases: undefined }
		})

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(false)

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
