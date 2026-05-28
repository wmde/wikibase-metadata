import WikibaseDetailCard from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCard.vue'
import { WikibaseCategory, WikibaseType } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseDetailCard', async () => {
	it('renders loading properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
			global: { plugins: [vuetify] },
			props: { wikibase: undefined, loading: true }
		})

		const container = wrapper.find('div.wikibase-detail-card')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-card')
		expect(container.classes()).toContain('v-card--variant-outlined')
		expect(container.classes()).toContain('ma-0')
		expect(container.classes()).toContain('pa-6')

		expect(container.find('div.wikibase-detail-card-loader').exists()).toEqual(true)
	})

	it('renders no info properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
			global: { plugins: [vuetify] },
			props: { wikibase: undefined, loading: false }
		})

		const container = wrapper.find('div.wikibase-detail-card')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-card')
		expect(container.classes()).toContain('v-card--variant-outlined')
		expect(container.classes()).toContain('ma-0')
		expect(container.classes()).toContain('pa-6')

		expect(container.find('div.wikibase-detail-card-loader').exists()).toEqual(false)
	})

	it('renders wiki properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
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
					externalIdentifierObservations: {},
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
				},
				loading: false
			}
		})

		const container = wrapper.find('div.wikibase-detail-card')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-card')
		expect(container.classes()).toContain('v-card--variant-outlined')
		expect(container.classes()).toContain('ma-0')
		expect(container.classes()).toContain('pa-6')

		expect(container.find('div.wikibase-detail-card-loader').exists()).toEqual(false)

		const header = container.find('div.card-header')
		expect(header.exists()).toEqual(true)
		expect(header.classes()).toContain('v-container')

		expect(header.find('div.wikibase-title').exists()).toEqual(true)

		const tagContainer = header.find('div.tag-container')
		expect(tagContainer.exists()).toEqual(true)
		expect(tagContainer.classes()).toContain('v-container')
		expect(tagContainer.classes()).toContain('ma-0')
		expect(tagContainer.classes()).toContain('mb-4')
		expect(tagContainer.classes()).toContain('pa-0')
		expect(tagContainer.find('span.wikibase-category-chip').exists()).toEqual(true)
		expect(tagContainer.find('span.wikibase-type-chip').exists()).toEqual(true)

		expect(header.find('div.description').exists()).toEqual(true)

		expect(container.find('div.statistics-container').exists()).toEqual(true)
		expect(container.find('div.access-container').exists()).toEqual(true)
		expect(container.find('div.history-container').exists()).toEqual(true)
	})
})
