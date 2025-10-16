import NumStatBlock from '@/component/wikibase-table/wikibase-detail-card/NumStatBlock.vue'
import { vuetify } from '@/main'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('NumStatBlock', async () => {
	it('renders populated stat properly', async () => {
		const wrapper = mount(NumStatBlock, {
			global: { plugins: [vuetify] },
			props: { label: 'Test Label', stat: 2000 }
		})

		const container = wrapper.find('div.stat-container')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-container')
		expect(container.classes()).toContain('pa-0')

		const label = container.find('label.stat-label')
		expect(label.exists()).toEqual(true)
		expect(label.classes()).toContain('v-label')
		expect(label.text()).toEqual('Test Label')

		const stat = container.find('div.stat')
		expect(stat.exists()).toEqual(true)
		expect(stat.text()).toEqual('2.000')
	})

	it('renders null stat properly', async () => {
		const wrapper = mount(NumStatBlock, {
			global: { plugins: [vuetify] },
			props: { label: 'Test Label', stat: null }
		})

		const container = wrapper.find('div.stat-container')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-container')
		expect(container.classes()).toContain('pa-0')

		const label = container.find('label.stat-label')
		expect(label.exists()).toEqual(true)
		expect(label.classes()).toContain('v-label')
		expect(label.text()).toEqual('Test Label')

		const stat = container.find('div.stat')
		expect(stat.exists()).toEqual(true)
		expect(stat.text()).toEqual('–')
	})

	it('renders undefined stat properly', async () => {
		const wrapper = mount(NumStatBlock, {
			global: { plugins: [vuetify] },
			props: { label: 'Test Label', stat: undefined }
		})

		const container = wrapper.find('div.stat-container')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-container')
		expect(container.classes()).toContain('pa-0')

		const label = container.find('label.stat-label')
		expect(label.exists()).toEqual(true)
		expect(label.classes()).toContain('v-label')
		expect(label.text()).toEqual('Test Label')

		const stat = container.find('div.stat')
		expect(stat.exists()).toEqual(true)
		expect(stat.text()).toEqual('–')
	})
})
