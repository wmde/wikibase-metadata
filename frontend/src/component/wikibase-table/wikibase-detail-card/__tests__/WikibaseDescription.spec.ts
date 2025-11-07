import WikibaseDescription from '@/component/wikibase-table/wikibase-detail-card/WikibaseDescription.vue'
import { WikibaseCategory, WikibaseType } from '@/graphql/types'
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
					category: WikibaseCategory.FictionalAndCreativeWorks,
					description: 'A test description',
					urls: {
						baseUrl: 'https://test-wikibase-001.test'
					},
					quantityObservations: {},
					recentChangesObservations: {},
					timeToFirstValueObservations: {},
					wikibaseType: WikibaseType.Cloud
				}
			}
		})

		const tooltip = document.querySelector('.desc-tooltip')
		expect(tooltip).not.toBeNull()
		expect(tooltip?.textContent).toEqual('Manually written')

		const descContainer = wrapper.find('div.description')
		expect(descContainer.exists()).toEqual(true)
		expect(descContainer.classes()).toContain('v-container')
		expect(descContainer.classes()).toContain('ma-0')
		expect(descContainer.classes()).toContain('pa-1')
		expect(descContainer.text()).toEqual('A test description')
	})
})
