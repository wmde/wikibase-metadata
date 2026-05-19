import WikibaseStatistics from '@/component/wikibase-table/wikibase-detail-card/WikibaseStatistics.vue'
import { WikibaseCategory, WikibaseType } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseStatistics', async () => {
	it('renders wiki properly', async () => {
		const wrapper = mount(WikibaseStatistics, {
			global: { plugins: [vuetify] },
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
					externalIdentifierObservations: {
						mostRecent: {
							totalExternalIdentifierStatements: 5
						}
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

		const container = wrapper.find('div.statistics-container')
		expect(container.exists()).toEqual(true)

		const title = container.find('div.title')
		expect(title.exists()).toEqual(true)
		expect(title.text()).toEqual('Statistics')

		const subContainer = container.find('div.stats-container')
		expect(subContainer.exists()).toEqual(true)

		expect(subContainer.findAll('div.statistic')).toHaveLength(7)
		expect(subContainer.findAll('div.statistic')[0]?.find('div.statistic-label').text()).toEqual(
			'Total Triples'
		)
		expect(subContainer.findAll('div.statistic')[0]?.find('div.statistic-value').text()).toEqual(
			'5'
		)
		expect(subContainer.findAll('div.statistic')[1]?.find('div.statistic-label').text()).toEqual(
			'Edits (Last 30 days)'
		)
		expect(subContainer.findAll('div.statistic')[1]?.find('div.statistic-value').text()).toEqual(
			'21'
		)
		expect(subContainer.findAll('div.statistic')[2]?.find('div.statistic-label').text()).toEqual(
			'Items'
		)
		expect(subContainer.findAll('div.statistic')[2]?.find('div.statistic-value').text()).toEqual(
			'1'
		)
		expect(subContainer.findAll('div.statistic')[3]?.find('div.statistic-label').text()).toEqual(
			'Properties'
		)
		expect(subContainer.findAll('div.statistic')[3]?.find('div.statistic-value').text()).toEqual(
			'3'
		)
		expect(subContainer.findAll('div.statistic')[4]?.find('div.statistic-label').text()).toEqual(
			'Lexemes'
		)
		expect(subContainer.findAll('div.statistic')[4]?.find('div.statistic-value').text()).toEqual(
			'2'
		)
		expect(subContainer.findAll('div.statistic')[5]?.find('div.statistic-label').text()).toEqual(
			'External Identifiers'
		)
		expect(subContainer.findAll('div.statistic')[5]?.find('div.statistic-value').text()).toEqual(
			'5'
		)
		expect(subContainer.findAll('div.statistic')[6]?.find('div.statistic-label').text()).toEqual(
			'First Record'
		)
		expect(subContainer.findAll('div.statistic')[6]?.find('div.statistic-value').text()).toEqual(
			'1.1.1970 00:00:00'
		)
	})
})
