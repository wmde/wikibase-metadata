import WikibaseDetailStats from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailStats.vue'
import { WikibaseCategory, WikibaseType } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('WikibaseDetailStats', async () => {
	beforeEach(() => setActivePinia(createPinia()))

	it('renders cloud wiki properly', async () => {
		const wrapper = mount(WikibaseDetailStats, {
			global: { mocks: { Image: vi.mockObject(Image) }, plugins: [vuetify] },
			props: {
				wikibase: {
					id: '1',
					title: 'Test Wikibase',
					category: WikibaseCategory.FictionalAndCreativeWorks,
					description: 'A test description',
					urls: {
						baseUrl: 'https://test-wikibase-001.test',
						sparqlFrontendUrl: 'https://test-wikibase-001.test/query'
					},
					quantityObservations: {
						mostRecent: {
							id: '-1',
							observationDate: new Date(0),
							totalItems: 1,
							totalLexemes: 2,
							totalProperties: 3,
							totalTriples: 5
						}
					},
					recentChangesObservations: {
						mostRecent: {
							id: '-1',
							observationDate: new Date(0),
							botChangeCount: 8,
							humanChangeCount: 13
						}
					},
					timeToFirstValueObservations: {
						mostRecent: { id: '-1', initiationDate: new Date(0), itemDates: [] }
					},
					wikibaseType: WikibaseType.Cloud
				}
			}
		})

		const table = wrapper.find('div.wikibase-detail-stats')
		expect(table.exists()).toEqual(true)
		expect(table.classes()).toContain('v-table')

		expect(table.find('tbody').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr').length).toEqual(8)

		expect(table.find('tbody').findAll('tr')[0]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[0]?.find('th').text()).toEqual('FIRST RECORD')
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[0]?.text()).toEqual(
			'1.1.1970 01:00:00'
		)
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[1]?.text()).toEqual('Action API')
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[1]?.attributes()).toHaveProperty(
			'rowspan',
			'1'
		)

		expect(table.find('tbody').findAll('tr')[1]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[1]?.find('th').text()).toEqual('ITEMS')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[0]?.text()).toEqual('1')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[1]?.text()).toEqual('Query Service')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[1]?.attributes()).toHaveProperty(
			'rowspan',
			'5'
		)

		expect(table.find('tbody').findAll('tr')[2]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[2]?.find('th').text()).toEqual('PROPERTIES')
		expect(table.find('tbody').findAll('tr')[2]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[2]?.findAll('td')[0]?.text()).toEqual('3')

		expect(table.find('tbody').findAll('tr')[3]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[3]?.find('th').text()).toEqual('LEXEMES')
		expect(table.find('tbody').findAll('tr')[3]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[3]?.findAll('td')[0]?.text()).toEqual('2')

		expect(table.find('tbody').findAll('tr')[4]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[4]?.find('th').text()).toEqual('TRIPLES')
		expect(table.find('tbody').findAll('tr')[4]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[4]?.findAll('td')[0]?.text()).toEqual('5')

		expect(table.find('tbody').findAll('tr')[5]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[5]?.find('th').text()).toEqual('AS OF')
		expect(table.find('tbody').findAll('tr')[5]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[5]?.findAll('td')[0]?.text()).toEqual('1.1.1970')

		expect(table.find('tbody').findAll('tr')[6]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[6]?.find('th').text()).toEqual('EDITS (LAST 30 DAYS)')
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[0]?.text()).toEqual('21')
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[1]?.text()).toEqual('Action API')
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[1]?.attributes()).toHaveProperty(
			'rowspan',
			'2'
		)

		expect(table.find('tbody').findAll('tr')[7]?.isVisible()).toEqual(false)
		expect(table.find('tbody').findAll('tr')[7]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[7]?.find('th').text()).toEqual('AS OF')
		expect(table.find('tbody').findAll('tr')[7]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[7]?.findAll('td')[0]?.text()).toEqual('1.1.1970')
	})

	it('renders suite wiki properly', async () => {
		const wrapper = mount(WikibaseDetailStats, {
			global: { mocks: { Image: vi.mockObject(Image) }, plugins: [vuetify] },
			props: {
				wikibase: {
					id: '1',
					title: 'Test Wikibase',
					description: 'A test description',
					urls: {
						baseUrl: 'https://test-wikibase-001.test',
						sparqlFrontendUrl: 'https://test-wikibase-001.test/query'
					},
					quantityObservations: {
						mostRecent: {
							id: '-1',
							observationDate: new Date(0),
							totalItems: 1,
							totalLexemes: 2,
							totalProperties: 3,
							totalTriples: 5
						}
					},
					recentChangesObservations: {
						mostRecent: {
							id: '-1',
							observationDate: new Date(0),
							botChangeCount: 8,
							humanChangeCount: 13
						}
					},
					timeToFirstValueObservations: {
						mostRecent: { id: '-1', initiationDate: new Date(0), itemDates: [] }
					},
					wikibaseType: WikibaseType.Suite
				}
			}
		})

		const table = wrapper.find('div.wikibase-detail-stats')
		expect(table.exists()).toEqual(true)
		expect(table.classes()).toContain('v-table')

		expect(table.find('tbody').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr').length).toEqual(8)

		expect(table.find('tbody').findAll('tr')[0]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[0]?.find('th').text()).toEqual('FIRST RECORD')
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[0]?.text()).toEqual(
			'1.1.1970 01:00:00'
		)
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[1]?.text()).toEqual('Action API')
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[1]?.attributes()).toHaveProperty(
			'rowspan',
			'1'
		)

		expect(table.find('tbody').findAll('tr')[1]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[1]?.find('th').text()).toEqual('ITEMS')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[0]?.text()).toEqual('1')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[1]?.text()).toEqual('Query Service')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[1]?.attributes()).toHaveProperty(
			'rowspan',
			'5'
		)

		expect(table.find('tbody').findAll('tr')[2]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[2]?.find('th').text()).toEqual('PROPERTIES')
		expect(table.find('tbody').findAll('tr')[2]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[2]?.findAll('td')[0]?.text()).toEqual('3')

		expect(table.find('tbody').findAll('tr')[3]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[3]?.find('th').text()).toEqual('LEXEMES')
		expect(table.find('tbody').findAll('tr')[3]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[3]?.findAll('td')[0]?.text()).toEqual('2')

		expect(table.find('tbody').findAll('tr')[4]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[4]?.find('th').text()).toEqual('TRIPLES')
		expect(table.find('tbody').findAll('tr')[4]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[4]?.findAll('td')[0]?.text()).toEqual('5')

		expect(table.find('tbody').findAll('tr')[5]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[5]?.find('th').text()).toEqual('AS OF')
		expect(table.find('tbody').findAll('tr')[5]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[5]?.findAll('td')[0]?.text()).toEqual('1.1.1970')

		expect(table.find('tbody').findAll('tr')[6]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[6]?.find('th').text()).toEqual('EDITS (LAST 30 DAYS)')
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[0]?.text()).toEqual('21')
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[1]?.text()).toEqual('Action API')
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[1]?.attributes()).toHaveProperty(
			'rowspan',
			'2'
		)

		expect(table.find('tbody').findAll('tr')[7]?.isVisible()).toEqual(false)
		expect(table.find('tbody').findAll('tr')[7]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[7]?.find('th').text()).toEqual('AS OF')
		expect(table.find('tbody').findAll('tr')[7]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[7]?.findAll('td')[0]?.text()).toEqual('1.1.1970')
	})

	it('renders unknown wiki properly', async () => {
		const wrapper = mount(WikibaseDetailStats, {
			global: { mocks: { Image: vi.mockObject(Image) }, plugins: [vuetify] },
			props: {
				wikibase: {
					id: '1',
					title: 'Test Wikibase',
					description: 'A test description',
					urls: {
						baseUrl: 'https://test-wikibase-001.test',
						sparqlFrontendUrl: 'https://test-wikibase-001.test/query'
					},
					quantityObservations: { mostRecent: { id: '-1', observationDate: new Date(0) } },
					recentChangesObservations: { mostRecent: { id: '-1', observationDate: new Date(0) } },
					timeToFirstValueObservations: {
						mostRecent: {
							id: '-1',
							initiationDate: new Date(0),
							itemDates: [
								{ id: '1', q: 1, creationDate: new Date(1000) },
								{ id: '2', q: 10, creationDate: new Date(2000) },
								{ id: '3', q: 100, creationDate: new Date(3000) }
							]
						}
					},
					wikibaseType: WikibaseType.Unknown
				},
				loading: false
			}
		})

		const table = wrapper.find('div.wikibase-detail-stats')
		expect(table.exists()).toEqual(true)
		expect(table.classes()).toContain('v-table')

		expect(table.find('thead').exists()).toEqual(true)
		expect(table.find('thead').findAll('tr').length).toEqual(1)
		expect(table.find('thead').findAll('tr')[0]?.findAll('th').length).toEqual(2)
		expect(table.find('thead').findAll('tr')[0]?.findAll('th')[0]?.attributes()).toHaveProperty(
			'colspan',
			'2'
		)
		expect(table.find('thead').findAll('tr')[0]?.findAll('th')[0]?.text()).toEqual('STATISTIC')
		expect(table.find('thead').findAll('tr')[0]?.findAll('th')[1]?.text()).toEqual('SOURCE')

		expect(table.find('tbody').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr').length).toEqual(11)

		expect(table.find('tbody').findAll('tr')[0]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[0]?.find('th').text()).toEqual('FIRST RECORD')
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[0]?.text()).toEqual(
			'1.1.1970 01:00:00'
		)
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[1]?.text()).toEqual('Action API')
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[1]?.attributes()).toHaveProperty(
			'rowspan',
			'4'
		)

		expect(table.find('tbody').findAll('tr')[1]?.find('th').exists()).toEqual(false)
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[0]?.text()).toEqual('Q1')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[1]?.text()).toEqual(
			'1.1.1970 01:00:01'
		)

		expect(table.find('tbody').findAll('tr')[2]?.find('th').exists()).toEqual(false)
		expect(table.find('tbody').findAll('tr')[2]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[2]?.findAll('td')[0]?.text()).toEqual('Q10')
		expect(table.find('tbody').findAll('tr')[2]?.findAll('td')[1]?.text()).toEqual(
			'1.1.1970 01:00:02'
		)

		expect(table.find('tbody').findAll('tr')[3]?.find('th').exists()).toEqual(false)
		expect(table.find('tbody').findAll('tr')[3]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[3]?.findAll('td')[0]?.text()).toEqual('Q100')
		expect(table.find('tbody').findAll('tr')[3]?.findAll('td')[1]?.text()).toEqual(
			'1.1.1970 01:00:03'
		)

		expect(table.find('tbody').findAll('tr')[4]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[4]?.find('th').text()).toEqual('ITEMS')
		expect(table.find('tbody').findAll('tr')[4]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[4]?.findAll('td')[0]?.text()).toEqual('–')
		expect(table.find('tbody').findAll('tr')[4]?.findAll('td')[1]?.text()).toEqual('Query Service')
		expect(table.find('tbody').findAll('tr')[4]?.findAll('td')[1]?.attributes()).toHaveProperty(
			'rowspan',
			'5'
		)

		expect(table.find('tbody').findAll('tr')[5]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[5]?.find('th').text()).toEqual('PROPERTIES')
		expect(table.find('tbody').findAll('tr')[5]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[5]?.findAll('td')[0]?.text()).toEqual('–')

		expect(table.find('tbody').findAll('tr')[6]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[6]?.find('th').text()).toEqual('LEXEMES')
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[0]?.text()).toEqual('–')

		expect(table.find('tbody').findAll('tr')[7]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[7]?.find('th').text()).toEqual('TRIPLES')
		expect(table.find('tbody').findAll('tr')[7]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[7]?.findAll('td')[0]?.text()).toEqual('–')

		expect(table.find('tbody').findAll('tr')[8]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[8]?.find('th').text()).toEqual('AS OF')
		expect(table.find('tbody').findAll('tr')[8]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[8]?.findAll('td')[0]?.text()).toEqual('1.1.1970')

		expect(table.find('tbody').findAll('tr')[9]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[9]?.find('th').text()).toEqual('EDITS (LAST 30 DAYS)')
		expect(table.find('tbody').findAll('tr')[9]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[9]?.findAll('td')[0]?.text()).toEqual('–')
		expect(table.find('tbody').findAll('tr')[9]?.findAll('td')[1]?.text()).toEqual('Action API')
		expect(table.find('tbody').findAll('tr')[9]?.findAll('td')[1]?.attributes()).toHaveProperty(
			'rowspan',
			'2'
		)

		expect(table.find('tbody').findAll('tr')[10]?.isVisible()).toEqual(false)
		expect(table.find('tbody').findAll('tr')[10]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[10]?.find('th').text()).toEqual('AS OF')
		expect(table.find('tbody').findAll('tr')[10]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[10]?.findAll('td')[0]?.text()).toEqual('1.1.1970')
	})
})
