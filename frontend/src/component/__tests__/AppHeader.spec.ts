import AppHeader from '@/component/AppHeader.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('AppHeader', async () => {
	it('renders properly', async () => {
		const wrapper = mount(AppHeader, { global: { plugins: [vuetify] } })

		const headerContainer = wrapper.find('div.header')
		expect(headerContainer.exists()).toEqual(true)

		const leftSection = headerContainer.find('div.left-header')
		expect(leftSection.exists()).toEqual(true)
		expect(leftSection.classes()).toContain('shrink')

		const iconContainer = leftSection.find('div.icon')
		expect(iconContainer.exists()).toEqual(true)
		expect(iconContainer.classes()).toContain('shrink')

		const titleContainer = leftSection.find('div.title')
		expect(titleContainer.classes()).toContain('v-container')
		expect(titleContainer.classes()).toContain('ma-0')
		expect(titleContainer.classes()).toContain('pa-0')
		expect(titleContainer.classes()).toContain('shrink')

		expect(titleContainer.text()).toEqual('Wikibase Ecosystem')

		const rightSection = headerContainer.find('div.right-header')
		expect(rightSection.exists()).toEqual(true)
		expect(rightSection.classes()).toContain('shrink')

		const themeButton = rightSection.find('button.theme-switch')
		expect(themeButton.exists()).toEqual(true)
		expect(themeButton.find('i.v-icon').exists()).toEqual(true)
	})
})
