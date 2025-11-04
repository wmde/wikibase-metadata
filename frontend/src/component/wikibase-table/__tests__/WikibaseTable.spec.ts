import { ResizeObserverMock } from '@/__tests__/global-mocks'
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import { WikibaseCategory, WikibaseType, type WbFragment } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
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

const mockSetSort = vi.fn().mockName('sortByColumn')

vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiStore: (): WikibasePageStoreType => ({
		...mockWikiStore,
		setSort: mockSetSort,
		wikibasePage: {
			...mockWikiStore.wikibasePage,
			data: {
				meta: { totalCount: testWikibasesAlt.length },
				data: testWikibasesAlt.sort(
					(a, b) =>
						(b.quantityObservations.mostRecent?.totalTriples ?? 0) -
						(a.quantityObservations.mostRecent?.totalTriples ?? 0)
				)
			}
		}
	})
}))

describe('WikibaseTable', async () => {
	beforeEach(() => setActivePinia(createPinia()))

	it('renders data properly', async () => {
		const wrapper = mount(WikibaseTable, { global: { plugins: [vuetify] } })

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
		).toEqual(['–', 'FICTIONAL_AND_CREATIVE_WORKS', '–', '–', 'TECHNOLOGY_AND_OPEN_SOURCE'])
		expect(
			table
				.find('tbody')
				.findAll('tr')
				.map((tr) => tr.findAll('td')[6]?.text())
		).toEqual(['–', '–', '–', 'An Example for the Purposes of Testing', '–'])
	})

	it.todo('triggers change page', async () => {
		// const wrapper = mount(WikibaseTable, {			global: { plugins: [vuetify] }		})
	})

	it.todo('triggers change page size', async () => {
		// const wrapper = mount(WikibaseTable, {			global: { plugins: [vuetify] }		})
	})

	it('triggers sort', async () => {
		const wrapper = mount(WikibaseTable, { global: { plugins: [vuetify] } })

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(false)

		const tableContainer = wrapper.find('div.wikibase-table')
		expect(tableContainer.exists()).toEqual(true)

		const table = tableContainer.find('table')
		expect(table.exists()).toEqual(true)

		const tableHead = table.find('thead')
		expect(tableHead.exists()).toEqual(true)
		expect(tableHead.findAll('tr').length).toEqual(1)
		expect(tableHead.find('tr').findAll('th').length).toEqual(8)
		expect(tableHead.find('tr').findAll('th')[4]?.text()).toEqual('Edits')

		expect(mockSetSort).toHaveBeenCalledTimes(0)

		await tableHead.find('tr').findAll('th')[4]?.trigger('click')
		await nextTick()

		expect(mockSetSort).toHaveBeenCalledTimes(1)
		expect(mockSetSort).toHaveBeenCalledWith({ column: 'EDITS', dir: 'ASC' })
	})
})
