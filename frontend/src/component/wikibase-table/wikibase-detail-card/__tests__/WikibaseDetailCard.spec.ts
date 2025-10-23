import WikibaseDetailCard from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCard.vue'
import { WikibaseType } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

describe('WikibaseDetailCard', async () => {
	beforeEach(() => setActivePinia(createPinia()))

	it('renders no info properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
			global: { plugins: [vuetify] },
			props: { wikibase: undefined, loading: false }
		})

		const container = wrapper.find('div.wikibase-detail-card')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-card')
		expect(container.classes()).toContain('v-card--variant-outlined')
		expect(container.classes()).toContain('ma-1')
		expect(container.classes()).toContain('pa-1')

		expect(container.text()).not.toContain('LOADING')
	})

	it('renders cloud wiki properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
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
					wikibaseType: WikibaseType.Cloud
				},
				loading: false
			}
		})

		const container = wrapper.find('div.wikibase-detail-card')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-card')
		expect(container.classes()).toContain('v-card--variant-outlined')
		expect(container.classes()).toContain('ma-1')
		expect(container.classes()).toContain('pa-1')

		expect(container.text()).not.toContain('LOADING')

		const header = container.find('div.card-header')
		expect(header.exists()).toEqual(true)
		expect(header.classes()).toContain('v-container')

		const urlContainer = header.find('div.url-container')
		expect(urlContainer.exists()).toEqual(true)
		expect(urlContainer.classes()).toContain('v-container')
		expect(urlContainer.classes()).toContain('ma-0')
		expect(urlContainer.classes()).toContain('pa-0')

		expect(urlContainer.findAll('div.wikibase-url').length).toEqual(2)

		const wikibaseUrlContainer = urlContainer.findAll('div.wikibase-url')[0]
		expect(wikibaseUrlContainer?.exists()).toEqual(true)
		expect(wikibaseUrlContainer?.classes()).toContain('v-container')
		expect(wikibaseUrlContainer?.classes()).toContain('ma-0')
		expect(wikibaseUrlContainer?.classes()).toContain('pa-0')

		const wikibaseLink = wikibaseUrlContainer?.find('a')
		expect(wikibaseLink?.exists()).toEqual(true)
		expect(wikibaseLink?.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test')
		expect(wikibaseLink?.text()).toEqual('Test Wikibase')

		const sparqlUrlContainer = urlContainer.findAll('div.wikibase-url')[1]
		expect(sparqlUrlContainer?.exists()).toEqual(true)
		expect(sparqlUrlContainer?.classes()).toContain('v-container')
		expect(sparqlUrlContainer?.classes()).toContain('ma-0')
		expect(sparqlUrlContainer?.classes()).toContain('pa-0')

		const sparqlLink = sparqlUrlContainer?.find('a')
		expect(sparqlLink?.exists()).toEqual(true)
		expect(sparqlLink?.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test/query')
		expect(sparqlLink?.text()).toEqual('SPARQL')

		const descriptionContainer = header.find('div.description')
		expect(descriptionContainer.exists()).toEqual(true)
		expect(descriptionContainer.classes()).toContain('v-container')
		expect(descriptionContainer.text()).toEqual('A test description')

		const wikibaseTypeContainer = header.find('div.wikibase-type')
		expect(wikibaseTypeContainer.exists()).toEqual(true)
		expect(wikibaseTypeContainer.classes()).toContain('v-container')

		const wikibaseTypeChip = wikibaseTypeContainer.find('span.wikibase-type-chip')
		expect(wikibaseTypeChip.exists()).toEqual(true)
		expect(wikibaseTypeChip.classes()).toContain('v-chip')
		expect(wikibaseTypeChip.text()).toEqual('CLOUD')

		expect(container.findAll('div.stat-block-container').length).toEqual(3)

		const creationContainer = container.findAll('div.stat-block-container')[0]
		expect(creationContainer?.exists()).toEqual(true)
		expect(creationContainer?.findAll('div.stat-container').length).toEqual(2)

		expect(creationContainer?.findAll('div.stat-container')[0]?.exists()).toEqual(true)
		expect(
			creationContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			creationContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').text()
		).toEqual('FIRST RECORD')
		expect(creationContainer?.findAll('div.stat-container')[0]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(creationContainer?.findAll('div.stat-container')[0]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)

		expect(creationContainer?.findAll('div.stat-container')[1]?.exists()).toEqual(true)
		expect(
			creationContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			creationContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').text()
		).toEqual('AS OF')
		expect(creationContainer?.findAll('div.stat-container')[1]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(creationContainer?.findAll('div.stat-container')[1]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)

		const quantityContainer = container.findAll('div.stat-block-container')[1]
		expect(quantityContainer?.exists()).toEqual(true)
		expect(quantityContainer?.findAll('div.stat-container').length).toEqual(5)

		expect(quantityContainer?.findAll('div.stat-container')[0]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').text()
		).toEqual('ITEMS')
		expect(quantityContainer?.findAll('div.stat-container')[0]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[0]?.find('div.stat').text()).toEqual(
			'1'
		)

		expect(quantityContainer?.findAll('div.stat-container')[1]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').text()
		).toEqual('PROPERTIES')
		expect(quantityContainer?.findAll('div.stat-container')[1]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[1]?.find('div.stat').text()).toEqual(
			'3'
		)

		expect(quantityContainer?.findAll('div.stat-container')[2]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[2]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[2]?.find('label.stat-label').text()
		).toEqual('LEXEMES')
		expect(quantityContainer?.findAll('div.stat-container')[2]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[2]?.find('div.stat').text()).toEqual(
			'2'
		)

		expect(quantityContainer?.findAll('div.stat-container')[3]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[3]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[3]?.find('label.stat-label').text()
		).toEqual('TRIPLES')
		expect(quantityContainer?.findAll('div.stat-container')[3]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[3]?.find('div.stat').text()).toEqual(
			'5'
		)

		expect(quantityContainer?.findAll('div.stat-container')[4]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[4]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[4]?.find('label.stat-label').text()
		).toEqual('AS OF')
		expect(quantityContainer?.findAll('div.stat-container')[4]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[4]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)

		const editsContainer = container.findAll('div.stat-block-container')[2]
		expect(editsContainer?.exists()).toEqual(true)
		expect(editsContainer?.findAll('div.stat-container').length).toEqual(2)

		expect(editsContainer?.findAll('div.stat-container')[0]?.exists()).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').text()
		).toEqual('EDITS (30 DAYS)')
		expect(editsContainer?.findAll('div.stat-container')[0]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(editsContainer?.findAll('div.stat-container')[0]?.find('div.stat').text()).toEqual('21')

		expect(editsContainer?.findAll('div.stat-container')[1]?.exists()).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').text()
		).toEqual('AS OF')
		expect(editsContainer?.findAll('div.stat-container')[1]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(editsContainer?.findAll('div.stat-container')[1]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)
	})

	it('renders suite wiki properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
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
				},
				loading: false
			}
		})

		const container = wrapper.find('div.wikibase-detail-card')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-card')
		expect(container.classes()).toContain('v-card--variant-outlined')
		expect(container.classes()).toContain('ma-1')
		expect(container.classes()).toContain('pa-1')

		expect(container.text()).not.toContain('LOADING')

		const header = container.find('div.card-header')
		expect(header.exists()).toEqual(true)
		expect(header.classes()).toContain('v-container')

		const urlContainer = header.find('div.url-container')
		expect(urlContainer.exists()).toEqual(true)
		expect(urlContainer.classes()).toContain('v-container')
		expect(urlContainer.classes()).toContain('ma-0')
		expect(urlContainer.classes()).toContain('pa-0')

		expect(urlContainer.findAll('div.wikibase-url').length).toEqual(2)

		const wikibaseUrlContainer = urlContainer.findAll('div.wikibase-url')[0]
		expect(wikibaseUrlContainer?.exists()).toEqual(true)
		expect(wikibaseUrlContainer?.classes()).toContain('v-container')
		expect(wikibaseUrlContainer?.classes()).toContain('ma-0')
		expect(wikibaseUrlContainer?.classes()).toContain('pa-0')

		const wikibaseLink = wikibaseUrlContainer?.find('a')
		expect(wikibaseLink?.exists()).toEqual(true)
		expect(wikibaseLink?.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test')
		expect(wikibaseLink?.text()).toEqual('Test Wikibase')

		const sparqlUrlContainer = urlContainer.findAll('div.wikibase-url')[1]
		expect(sparqlUrlContainer?.exists()).toEqual(true)
		expect(sparqlUrlContainer?.classes()).toContain('v-container')
		expect(sparqlUrlContainer?.classes()).toContain('ma-0')
		expect(sparqlUrlContainer?.classes()).toContain('pa-0')

		const sparqlLink = sparqlUrlContainer?.find('a')
		expect(sparqlLink?.exists()).toEqual(true)
		expect(sparqlLink?.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test/query')
		expect(sparqlLink?.text()).toEqual('SPARQL')

		const descriptionContainer = header.find('div.description')
		expect(descriptionContainer.exists()).toEqual(true)
		expect(descriptionContainer.classes()).toContain('v-container')
		expect(descriptionContainer.text()).toEqual('A test description')

		const wikibaseTypeContainer = header.find('div.wikibase-type')
		expect(wikibaseTypeContainer.exists()).toEqual(true)
		expect(wikibaseTypeContainer.classes()).toContain('v-container')

		const wikibaseTypeChip = wikibaseTypeContainer.find('span.wikibase-type-chip')
		expect(wikibaseTypeChip.exists()).toEqual(true)
		expect(wikibaseTypeChip.classes()).toContain('v-chip')
		expect(wikibaseTypeChip.text()).toEqual('SUITE')

		expect(container.findAll('div.stat-block-container').length).toEqual(3)

		const creationContainer = container.findAll('div.stat-block-container')[0]
		expect(creationContainer?.exists()).toEqual(true)
		expect(creationContainer?.findAll('div.stat-container').length).toEqual(2)

		expect(creationContainer?.findAll('div.stat-container')[0]?.exists()).toEqual(true)
		expect(
			creationContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			creationContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').text()
		).toEqual('FIRST RECORD')
		expect(creationContainer?.findAll('div.stat-container')[0]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(creationContainer?.findAll('div.stat-container')[0]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)

		expect(creationContainer?.findAll('div.stat-container')[1]?.exists()).toEqual(true)
		expect(
			creationContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			creationContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').text()
		).toEqual('AS OF')
		expect(creationContainer?.findAll('div.stat-container')[1]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(creationContainer?.findAll('div.stat-container')[1]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)

		const quantityContainer = container.findAll('div.stat-block-container')[1]
		expect(quantityContainer?.exists()).toEqual(true)
		expect(quantityContainer?.findAll('div.stat-container').length).toEqual(5)

		expect(quantityContainer?.findAll('div.stat-container')[0]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').text()
		).toEqual('ITEMS')
		expect(quantityContainer?.findAll('div.stat-container')[0]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[0]?.find('div.stat').text()).toEqual(
			'1'
		)

		expect(quantityContainer?.findAll('div.stat-container')[1]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').text()
		).toEqual('PROPERTIES')
		expect(quantityContainer?.findAll('div.stat-container')[1]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[1]?.find('div.stat').text()).toEqual(
			'3'
		)

		expect(quantityContainer?.findAll('div.stat-container')[2]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[2]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[2]?.find('label.stat-label').text()
		).toEqual('LEXEMES')
		expect(quantityContainer?.findAll('div.stat-container')[2]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[2]?.find('div.stat').text()).toEqual(
			'2'
		)

		expect(quantityContainer?.findAll('div.stat-container')[3]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[3]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[3]?.find('label.stat-label').text()
		).toEqual('TRIPLES')
		expect(quantityContainer?.findAll('div.stat-container')[3]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[3]?.find('div.stat').text()).toEqual(
			'5'
		)

		expect(quantityContainer?.findAll('div.stat-container')[4]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[4]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[4]?.find('label.stat-label').text()
		).toEqual('AS OF')
		expect(quantityContainer?.findAll('div.stat-container')[4]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[4]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)

		const editsContainer = container.findAll('div.stat-block-container')[2]
		expect(editsContainer?.exists()).toEqual(true)
		expect(editsContainer?.findAll('div.stat-container').length).toEqual(2)

		expect(editsContainer?.findAll('div.stat-container')[0]?.exists()).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').text()
		).toEqual('EDITS (30 DAYS)')
		expect(editsContainer?.findAll('div.stat-container')[0]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(editsContainer?.findAll('div.stat-container')[0]?.find('div.stat').text()).toEqual('21')

		expect(editsContainer?.findAll('div.stat-container')[1]?.exists()).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').text()
		).toEqual('AS OF')
		expect(editsContainer?.findAll('div.stat-container')[1]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(editsContainer?.findAll('div.stat-container')[1]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)
	})

	it('renders undefined wiki properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
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

		const container = wrapper.find('div.wikibase-detail-card')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-card')
		expect(container.classes()).toContain('v-card--variant-outlined')
		expect(container.classes()).toContain('ma-1')
		expect(container.classes()).toContain('pa-1')

		expect(container.text()).not.toContain('LOADING')

		const header = container.find('div.card-header')
		expect(header.exists()).toEqual(true)
		expect(header.classes()).toContain('v-container')

		const urlContainer = header.find('div.url-container')
		expect(urlContainer.exists()).toEqual(true)
		expect(urlContainer.classes()).toContain('v-container')
		expect(urlContainer.classes()).toContain('ma-0')
		expect(urlContainer.classes()).toContain('pa-0')

		expect(urlContainer.findAll('div.wikibase-url').length).toEqual(2)

		const wikibaseUrlContainer = urlContainer.findAll('div.wikibase-url')[0]
		expect(wikibaseUrlContainer?.exists()).toEqual(true)
		expect(wikibaseUrlContainer?.classes()).toContain('v-container')
		expect(wikibaseUrlContainer?.classes()).toContain('ma-0')
		expect(wikibaseUrlContainer?.classes()).toContain('pa-0')

		const wikibaseLink = wikibaseUrlContainer?.find('a')
		expect(wikibaseLink?.exists()).toEqual(true)
		expect(wikibaseLink?.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test')
		expect(wikibaseLink?.text()).toEqual('Test Wikibase')

		const sparqlUrlContainer = urlContainer.findAll('div.wikibase-url')[1]
		expect(sparqlUrlContainer?.exists()).toEqual(true)
		expect(sparqlUrlContainer?.classes()).toContain('v-container')
		expect(sparqlUrlContainer?.classes()).toContain('ma-0')
		expect(sparqlUrlContainer?.classes()).toContain('pa-0')

		const sparqlLink = sparqlUrlContainer?.find('a')
		expect(sparqlLink?.exists()).toEqual(true)
		expect(sparqlLink?.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test/query')
		expect(sparqlLink?.text()).toEqual('SPARQL')

		const descriptionContainer = header.find('div.description')
		expect(descriptionContainer.exists()).toEqual(true)
		expect(descriptionContainer.classes()).toContain('v-container')
		expect(descriptionContainer.text()).toEqual('A test description')

		const wikibaseTypeContainer = header.find('div.wikibase-type')
		expect(wikibaseTypeContainer.exists()).toEqual(true)
		expect(wikibaseTypeContainer.classes()).toContain('v-container')

		const wikibaseTypeChip = wikibaseTypeContainer.find('span.wikibase-type-chip')
		expect(wikibaseTypeChip.exists()).toEqual(true)
		expect(wikibaseTypeChip.classes()).toContain('v-chip')
		expect(wikibaseTypeChip.text()).toEqual('')

		expect(container.findAll('div.stat-block-container').length).toEqual(3)

		const creationContainer = container.findAll('div.stat-block-container')[0]
		expect(creationContainer?.exists()).toEqual(true)
		expect(creationContainer?.findAll('div.stat-container').length).toEqual(1)

		expect(creationContainer?.findAll('div.stat-container')[0]?.exists()).toEqual(true)
		expect(
			creationContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			creationContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').text()
		).toEqual('FIRST RECORD')
		expect(creationContainer?.findAll('div.stat-container')[0]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(creationContainer?.findAll('div.stat-container')[0]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)

		const quantityContainer = container.findAll('div.stat-block-container')[1]
		expect(quantityContainer?.exists()).toEqual(true)
		expect(quantityContainer?.findAll('div.stat-container').length).toEqual(5)

		expect(quantityContainer?.findAll('div.stat-container')[0]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').text()
		).toEqual('ITEMS')
		expect(quantityContainer?.findAll('div.stat-container')[0]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[0]?.find('div.stat').text()).toEqual(
			'–'
		)

		expect(quantityContainer?.findAll('div.stat-container')[1]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').text()
		).toEqual('PROPERTIES')
		expect(quantityContainer?.findAll('div.stat-container')[1]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[1]?.find('div.stat').text()).toEqual(
			'–'
		)

		expect(quantityContainer?.findAll('div.stat-container')[2]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[2]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[2]?.find('label.stat-label').text()
		).toEqual('LEXEMES')
		expect(quantityContainer?.findAll('div.stat-container')[2]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[2]?.find('div.stat').text()).toEqual(
			'–'
		)

		expect(quantityContainer?.findAll('div.stat-container')[3]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[3]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[3]?.find('label.stat-label').text()
		).toEqual('TRIPLES')
		expect(quantityContainer?.findAll('div.stat-container')[3]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[3]?.find('div.stat').text()).toEqual(
			'–'
		)

		expect(quantityContainer?.findAll('div.stat-container')[4]?.exists()).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[4]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			quantityContainer?.findAll('div.stat-container')[4]?.find('label.stat-label').text()
		).toEqual('AS OF')
		expect(quantityContainer?.findAll('div.stat-container')[4]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(quantityContainer?.findAll('div.stat-container')[4]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)

		const editsContainer = container.findAll('div.stat-block-container')[2]
		expect(editsContainer?.exists()).toEqual(true)
		expect(editsContainer?.findAll('div.stat-container').length).toEqual(2)

		expect(editsContainer?.findAll('div.stat-container')[0]?.exists()).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[0]?.find('label.stat-label').text()
		).toEqual('EDITS (30 DAYS)')
		expect(editsContainer?.findAll('div.stat-container')[0]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(editsContainer?.findAll('div.stat-container')[0]?.find('div.stat').text()).toEqual('–')

		expect(editsContainer?.findAll('div.stat-container')[1]?.exists()).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').exists()
		).toEqual(true)
		expect(
			editsContainer?.findAll('div.stat-container')[1]?.find('label.stat-label').text()
		).toEqual('AS OF')
		expect(editsContainer?.findAll('div.stat-container')[1]?.find('div.stat').exists()).toEqual(
			true
		)
		expect(editsContainer?.findAll('div.stat-container')[1]?.find('div.stat').text()).toEqual(
			'1.1.1970'
		)
	})

	it('renders loading properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
			global: { plugins: [vuetify] },
			props: { wikibase: undefined, loading: true }
		})

		const container = wrapper.find('div.wikibase-detail-card')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-card')
		expect(container.classes()).toContain('v-card--variant-outlined')
		expect(container.classes()).toContain('ma-1')
		expect(container.classes()).toContain('pa-1')

		expect(container.text()).toContain('LOADING')
	})
})
