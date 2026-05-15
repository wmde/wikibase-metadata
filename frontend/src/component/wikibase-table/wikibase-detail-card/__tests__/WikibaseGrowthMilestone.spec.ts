import WikibaseGrowthMilestone from '@/component/wikibase-table/wikibase-detail-card/WikibaseGrowthMilestone.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseGrowthMilestone', async () => {
	it('renders properly', async () => {
		const wrapper = mount(WikibaseGrowthMilestone, {
			global: { plugins: [vuetify] },
			props: { label: 'First Record', entities: 0, entityDate: new Date(2026, 5, 15) }
		})

		const container = wrapper.find('.milestone')
		expect(container.exists()).toEqual(true)

		const label = container.find('.milestone-q')
		expect(label.exists()).toEqual(true)
		expect(label.text()).toEqual('First Record')

		const entityCount = container.find('.milestone-count')
		expect(entityCount.exists()).toEqual(true)
		expect(entityCount.text()).toEqual('0 entities')

		const date = container.find('.milestone-date')
		expect(date.exists()).toEqual(true)
		expect(date.text()).toEqual('15.6.2026 00:00:00')
	})

	it('renders single entity', async () => {
		const wrapper = mount(WikibaseGrowthMilestone, {
			global: { plugins: [vuetify] },
			props: { label: 'First Record', entities: 1, entityDate: new Date(2026, 5, 15) }
		})

		const container = wrapper.find('.milestone')
		expect(container.exists()).toEqual(true)

		const label = container.find('.milestone-q')
		expect(label.exists()).toEqual(true)
		expect(label.text()).toEqual('First Record')

		const entityCount = container.find('.milestone-count')
		expect(entityCount.exists()).toEqual(true)
		expect(entityCount.text()).toEqual('1 entity')

		const date = container.find('.milestone-date')
		expect(date.exists()).toEqual(true)
		expect(date.text()).toEqual('15.6.2026 00:00:00')
	})

	it('renders multiple entity', async () => {
		const wrapper = mount(WikibaseGrowthMilestone, {
			global: { plugins: [vuetify] },
			props: { label: 'First Record', entities: 2, entityDate: new Date(2026, 5, 15) }
		})

		const container = wrapper.find('.milestone')
		expect(container.exists()).toEqual(true)

		const label = container.find('.milestone-q')
		expect(label.exists()).toEqual(true)
		expect(label.text()).toEqual('First Record')

		const entityCount = container.find('.milestone-count')
		expect(entityCount.exists()).toEqual(true)
		expect(entityCount.text()).toEqual('2 entities')

		const date = container.find('.milestone-date')
		expect(date.exists()).toEqual(true)
		expect(date.text()).toEqual('15.6.2026 00:00:00')
	})
})
