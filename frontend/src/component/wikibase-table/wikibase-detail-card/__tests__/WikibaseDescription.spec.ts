import WikibaseDescription from '@/component/wikibase-table/wikibase-detail-card/WikibaseDescription.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseDescription', async () => {
	it('renders description properly', async () => {
		const wrapper = mount(WikibaseDescription, {
			global: { plugins: [vuetify] },
			props: {
				wikibase: {
					id: '1',
					title: 'Test Wikibase',
					category: 'FICTIONAL_AND_CREATIVE_WORKS',
					description: 'A test description',
					urls: {
						baseUrl: 'https://test-wikibase-001.test',
						scriptPath: null,
						sparqlFrontendUrl: null
					},
					externalIdentifierObservations: { mostRecent: null },
					quantityObservations: { mostRecent: null },
					recentChangesObservations: { mostRecent: null },
					timeToFirstValueObservations: { mostRecent: null },
					wikibaseType: 'CLOUD'
				}
			}
		})

		const descContainer = wrapper.find('div.description')
		expect(descContainer.exists()).toEqual(true)
		expect(descContainer.classes()).toContain('v-container')
		expect(descContainer.classes()).toContain('ma-0')
		expect(descContainer.classes()).toContain('pa-0')
		expect(descContainer.text()).toEqual('A test description')
	})
})
