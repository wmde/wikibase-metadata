import { ResizeObserverMock } from '@/__tests__/global-mocks'
import testWikibases from '@/component/wikibase-table/__tests__/test-wikibases'
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import vuetify from '@/plugin/vuetify'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

const mockSetSort = vi.fn().mockName('sortByColumn')

vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiStore: (): WikibasePageStoreType => ({
		...mockWikiStore,
		setSort: mockSetSort,
		wikibasePage: {
			...mockWikiStore.wikibasePage,
			data: {
				meta: { totalCount: testWikibases.length },
				data: testWikibases.sort(
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
		).toEqual(['Unknown', 'Self-Hosted', 'Other', 'Wikibase Cloud', 'Self-Hosted'])
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
		).toEqual(['–', 'Fictional & Creative Works', '–', '–', 'Technology & Open Source'])
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

		const tableContainer = wrapper.find('div.wikibase-table')
		expect(tableContainer.exists()).toEqual(true)

		const table = tableContainer.find('table')
		expect(table.exists()).toEqual(true)

		const tableHead = table.find('thead')
		expect(tableHead.exists()).toEqual(true)
		expect(tableHead.findAll('tr').length).toEqual(1)
		expect(tableHead.find('tr').findAll('th').length).toEqual(8)
		expect(tableHead.find('tr').findAll('th')[4]?.text()).toEqual('Edits (last 30 days)')

		expect(mockSetSort).toHaveBeenCalledTimes(0)

		await tableHead.find('tr').findAll('th')[4]?.trigger('click')
		await nextTick()

		expect(mockSetSort).toHaveBeenCalledTimes(1)
		expect(mockSetSort).toHaveBeenCalledWith({ column: 'EDITS', dir: 'ASC' })
	})
})
