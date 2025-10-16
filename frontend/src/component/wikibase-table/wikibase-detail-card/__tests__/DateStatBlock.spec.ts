import DateStatBlock from '@/component/wikibase-table/wikibase-detail-card/DateStatBlock.vue'
import { vuetify } from '@/main'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('DateStatBlock', async () => {
	it('renders populated stat properly', async () => {
		const wrapper = mount(DateStatBlock, {
			global: { plugins: [vuetify] },
			props: { label: 'Test Label', stat: '2023-5-19' }
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
		expect(stat.text()).toEqual('19.5.2023')
	})

	it('renders null stat properly', async () => {
		const wrapper = mount(DateStatBlock, {
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
		const wrapper = mount(DateStatBlock, {
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
