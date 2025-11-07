import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import CardLoader from '../CardLoader.vue'

describe('CardLoader', async () => {
	it('renders properly', async () => {
		const wrapper = mount(CardLoader, { global: { plugins: [vuetify] } })

		const loader = wrapper.find('div.wikibase-detail-card-loader')
		expect(loader.exists()).toEqual(true)
		expect(loader.classes()).toContain('v-skeleton-loader')
	})
})
