import WikibaseGrowth from '@/component/wikibase-table/wikibase-detail-card/WikibaseGrowth.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseGrowth', async () => {
	it('renders nothing', async () => {
		const wrapper = mount(WikibaseGrowth, {
			global: { plugins: [vuetify] },
			props: {
				obs: {}
			}
		})

		const growthContainer = wrapper.find('.growth-container')
		expect(growthContainer.exists()).toEqual(false)
	})

	it('renders label properly', async () => {
		const wrapper = mount(WikibaseGrowth, {
			global: { plugins: [vuetify] },
			props: {
				obs: { initiationDate: new Date(2026, 5, 15) }
			}
		})

		const growthContainer = wrapper.find('.growth-container')
		expect(growthContainer.exists()).toEqual(true)
		expect(growthContainer.classes()).toContain('v-expansion-panels')
		expect(growthContainer.text()).toEqual('Growth Milestones')
	})

	it('renders label properly ii', async () => {
		const wrapper = mount(WikibaseGrowth, {
			global: { plugins: [vuetify] },
			props: {
				obs: { itemDates: [{ id: '1', q: 14, creationDate: new Date(2026, 6, 1) }] }
			}
		})

		const growthContainer = wrapper.find('.growth-container')
		expect(growthContainer.exists()).toEqual(true)
		expect(growthContainer.classes()).toContain('v-expansion-panels')
		expect(growthContainer.text()).toEqual('Growth Milestones')
	})

	it.todo('renders internal data properly - requires clicking to open expansion panel')
})
