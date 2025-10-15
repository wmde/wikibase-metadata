import AppHeader from '@/component/AppHeader.vue'
import { vuetify } from '@/main'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('AppHeader', async () => {
	it('renders properly', async () => {
		const wrapper = mount(AppHeader, { global: { plugins: [vuetify] } })

		const headerContainer = wrapper.find('div.header')
		expect(headerContainer.exists()).toEqual(true)

		const iconContainer = headerContainer.find('div.icon')
		expect(iconContainer.exists()).toEqual(true)

		const titleContainer = headerContainer.find('div.title')
		expect(titleContainer.classes()).toContain('v-container')
		expect(titleContainer.classes()).toContain('ma-0')
		expect(titleContainer.classes()).toContain('pa-0')

		expect(titleContainer.text()).toEqual('Suite Scraper')
	})
})
