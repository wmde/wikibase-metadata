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
							observationDate: new Date(0),
							totalItems: 1,
							totalLexemes: 2,
							totalProperties: 3,
							totalTriples: 5
						}
					},
					recentChangesObservations: {
						mostRecent: { observationDate: new Date(0), botChangeCount: 8, humanChangeCount: 13 }
					},
					timeToFirstValueObservations: { mostRecent: { initiationDate: new Date(0) } },
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
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[0]?.text()).toEqual('1.1.1970')
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[1]?.text()).toEqual(
			'Pulled from Action API'
		)

		expect(table.find('tbody').findAll('tr')[1]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[1]?.find('th').text()).toEqual('ITEMS')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[0]?.text()).toEqual('1')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[1]?.text()).toEqual(
			'Pulled from Query Service'
		)
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
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[1]?.text()).toEqual(
			'Pulled from Action API'
		)
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
							observationDate: new Date(0),
							totalItems: 1,
							totalLexemes: 2,
							totalProperties: 3,
							totalTriples: 5
						}
					},
					recentChangesObservations: {
						mostRecent: { observationDate: new Date(0), botChangeCount: 8, humanChangeCount: 13 }
					},
					timeToFirstValueObservations: { mostRecent: { initiationDate: new Date(0) } },
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
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[0]?.text()).toEqual('1.1.1970')
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[1]?.text()).toEqual(
			'Pulled from Action API'
		)

		expect(table.find('tbody').findAll('tr')[1]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[1]?.find('th').text()).toEqual('ITEMS')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[0]?.text()).toEqual('1')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[1]?.text()).toEqual(
			'Pulled from Query Service'
		)
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
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[1]?.text()).toEqual(
			'Pulled from Action API'
		)
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

	it('renders undefined wiki properly', async () => {
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
					quantityObservations: { mostRecent: { observationDate: new Date(0) } },
					recentChangesObservations: { mostRecent: { observationDate: new Date(0) } },
					timeToFirstValueObservations: { mostRecent: { initiationDate: new Date(0) } },
					wikibaseType: undefined
				},
				loading: false
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
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[0]?.text()).toEqual('1.1.1970')
		expect(table.find('tbody').findAll('tr')[0]?.findAll('td')[1]?.text()).toEqual(
			'Pulled from Action API'
		)

		expect(table.find('tbody').findAll('tr')[1]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[1]?.find('th').text()).toEqual('ITEMS')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[0]?.text()).toEqual('–')
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[1]?.text()).toEqual(
			'Pulled from Query Service'
		)
		expect(table.find('tbody').findAll('tr')[1]?.findAll('td')[1]?.attributes()).toHaveProperty(
			'rowspan',
			'5'
		)

		expect(table.find('tbody').findAll('tr')[2]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[2]?.find('th').text()).toEqual('PROPERTIES')
		expect(table.find('tbody').findAll('tr')[2]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[2]?.findAll('td')[0]?.text()).toEqual('–')

		expect(table.find('tbody').findAll('tr')[3]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[3]?.find('th').text()).toEqual('LEXEMES')
		expect(table.find('tbody').findAll('tr')[3]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[3]?.findAll('td')[0]?.text()).toEqual('–')

		expect(table.find('tbody').findAll('tr')[4]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[4]?.find('th').text()).toEqual('TRIPLES')
		expect(table.find('tbody').findAll('tr')[4]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[4]?.findAll('td')[0]?.text()).toEqual('–')

		expect(table.find('tbody').findAll('tr')[5]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[5]?.find('th').text()).toEqual('AS OF')
		expect(table.find('tbody').findAll('tr')[5]?.findAll('td').length).toEqual(1)
		expect(table.find('tbody').findAll('tr')[5]?.findAll('td')[0]?.text()).toEqual('1.1.1970')

		expect(table.find('tbody').findAll('tr')[6]?.find('th').exists()).toEqual(true)
		expect(table.find('tbody').findAll('tr')[6]?.find('th').text()).toEqual('EDITS (LAST 30 DAYS)')
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td').length).toEqual(2)
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[0]?.text()).toEqual('–')
		expect(table.find('tbody').findAll('tr')[6]?.findAll('td')[1]?.text()).toEqual(
			'Pulled from Action API'
		)
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
})
