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

	it('renders data properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
			global: {
				mocks: { Image: vi.mockObject(Image) },
				plugins: [vuetify]
			},
			props: {
				wikibase: {
					id: '1',
					title: 'Test Wikibase',
					urls: { baseUrl: 'https://test-wikibase-001.test' },
					quantityObservations: {},
					recentChangesObservations: {},
					timeToFirstValueObservations: {},
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
	})

	it('renders loading properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
			global: {
				plugins: [vuetify]
			},
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
