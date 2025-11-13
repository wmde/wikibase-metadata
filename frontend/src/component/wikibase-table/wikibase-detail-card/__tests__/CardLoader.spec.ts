import CardLoader from '@/component/wikibase-table/wikibase-detail-card/CardLoader.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('CardLoader', async () => {
	it('renders properly', async () => {
		const wrapper = mount(CardLoader, { global: { plugins: [vuetify] } })

		const loader = wrapper.find('div.wikibase-detail-card-loader')
		expect(loader.exists()).toEqual(true)
		expect(loader.classes()).toContain('v-skeleton-loader')
	})
})
