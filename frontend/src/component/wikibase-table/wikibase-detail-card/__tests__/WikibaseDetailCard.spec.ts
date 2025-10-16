import WikibaseDetailCard from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCard.vue'
import vuetify from '@/plugin/vuetify'
import mockSingleWikiStore from '@/stores/__tests__/mock-wikibase-store'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'

describe('WikibaseDetailCard', async () => {
	beforeEach(() => setActivePinia(createPinia()))

	it('renders no info properly', async () => {
		const wrapper = mount(WikibaseDetailCard, {
			global: { mocks: { useSingleWikiStore: () => mockSingleWikiStore }, plugins: [vuetify] },
			props: { wikibaseId: 1 }
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
				mocks: {
					useSingleWikiStore: () => ({
						...mockSingleWikiStore,
						wikibase: { ...mockSingleWikiStore.wikibase, loading: true }
					})
				},
				plugins: [vuetify]
			},
			props: { wikibaseId: 1 }
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
