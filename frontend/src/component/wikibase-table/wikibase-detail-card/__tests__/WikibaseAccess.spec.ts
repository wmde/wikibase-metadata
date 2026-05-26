import WikibaseAccess from '@/component/wikibase-table/wikibase-detail-card/WikibaseAccess.vue'
import { WikibaseCategory, WikibaseType } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseAccess', async () => {
	it('renders properly', async () => {
		const baseUrl = 'https://test-wikibase-001.test'
		const scriptPath = '/w'

		const wrapper = mount(WikibaseAccess, {
			global: { plugins: [vuetify] },
			props: {
				wikibase: {
					id: '1',
					title: 'Test Wikibase',
					category: WikibaseCategory.FictionalAndCreativeWorks,
					description: 'A test description',
					urls: {
						baseUrl: baseUrl,
						sparqlFrontendUrl: 'https://query.test-wikibase-001.test',
						scriptPath: scriptPath
					},
					externalIdentifierObservations: {},
					quantityObservations: {},
					recentChangesObservations: {},
					timeToFirstValueObservations: {},
					wikibaseType: WikibaseType.Cloud
				}
			}
		})

		const accessContainer = wrapper.find('div.access-container')
		expect(accessContainer.exists()).toEqual(true)
		expect(accessContainer.classes()).toContain('v-container')
		expect(accessContainer.classes()).toContain('ma-0')
		expect(accessContainer.classes()).toContain('pa-0')
		expect(accessContainer.classes()).toContain('pb-8')

		const titleContainer = accessContainer.find('div.title')
		expect(titleContainer.exists()).toEqual(true)
		expect(titleContainer.text()).toEqual('Access')

		const buttonContainer = accessContainer.find('div.acc-container')
		expect(buttonContainer.exists()).toEqual(true)
		expect(buttonContainer.findAll('.v-btn')).toHaveLength(3)

		expect(buttonContainer.findAll('.v-btn')[0]?.text()).toEqual('Visit Instance')
		expect(buttonContainer.findAll('.v-btn')[0]?.attributes()).toHaveProperty(
			'href',
			'https://test-wikibase-001.test'
		)
		expect(buttonContainer.findAll('.v-btn')[0]?.attributes()).toHaveProperty('target', '_blank')

		expect(buttonContainer.findAll('.v-btn')[1]?.text()).toEqual('Query Service')
		expect(buttonContainer.findAll('.v-btn')[1]?.attributes()).toHaveProperty(
			'href',
			'https://query.test-wikibase-001.test'
		)
		expect(buttonContainer.findAll('.v-btn')[1]?.attributes()).toHaveProperty('target', '_blank')

		const apiButton = buttonContainer.find('#api-button')
		expect(apiButton.text()).toEqual('API')
		expect(apiButton.attributes()).toHaveProperty('target', '_blank')
		expect(apiButton.attributes()).toHaveProperty('href', `${baseUrl}${scriptPath}/api.php`)
	})

	it("does not render API button if wikibase doesn't have a scriptPath", async () => {
		const wrapper = mount(WikibaseAccess, {
			global: { plugins: [vuetify] },
			props: {
				wikibase: {
					id: '1',
					title: 'Test Wikibase',
					category: WikibaseCategory.FictionalAndCreativeWorks,
					description: 'A test description',
					urls: {
						baseUrl: 'https://test-wikibase-001.test',
						sparqlFrontendUrl: 'https://query.test-wikibase-001.test'
					},
					externalIdentifierObservations: {},
					quantityObservations: {},
					recentChangesObservations: {},
					timeToFirstValueObservations: {},
					wikibaseType: WikibaseType.Cloud
				}
			}
		})

		const accessContainer = wrapper.find('div.access-container')
		const buttonContainer = accessContainer.find('div.acc-container')
		const apiButton = buttonContainer.find('#api-button')
		expect(apiButton.exists()).toEqual(false)
	})
})
