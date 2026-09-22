import SearchMenu from '@/component/wikibase-table/SearchMenu.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

const mockSetMenuValue = vi.fn().mockName('setMenuValue')

describe('SearchMenu', async () => {
	beforeEach(() => vi.resetAllMocks())

	it('renders properly', async () => {
		const wrapper = mount(SearchMenu, {
			global: { plugins: [vuetify] },
			props: { menuValue: 'items', setMenuValue: mockSetMenuValue }
		})

		const container = wrapper.find('.v-list')
		expect(container.exists()).toEqual(true)

		const items = container.findAll('.v-list-item')
		expect(items).toHaveLength(2)

		expect(items[0].text()).toEqual('Instances')
		expect(items[1].text()).toEqual('Items')
	})

	it('updates menuValue to Instances on click', async () => {
		const wrapper = mount(SearchMenu, {
			global: { plugins: [vuetify] },
			props: { menuValue: 'items', setMenuValue: mockSetMenuValue }
		})

		const container = wrapper.find('.v-list')
		const items = container.findAll('.v-list-item')

		expect(mockSetMenuValue).toHaveBeenCalledTimes(0)

		await items[0].trigger('click')
		await nextTick()

		expect(mockSetMenuValue).toHaveBeenCalledTimes(1)
		expect(mockSetMenuValue).toHaveBeenCalledWith('instances')
	})

	it('updates menuValue to Items on click', async () => {
		const wrapper = mount(SearchMenu, {
			global: { plugins: [vuetify] },
			props: { menuValue: 'instances', setMenuValue: mockSetMenuValue }
		})

		const container = wrapper.find('.v-list')
		const items = container.findAll('.v-list-item')

		expect(mockSetMenuValue).toHaveBeenCalledTimes(0)

		await items[1].trigger('click')
		await nextTick()

		expect(mockSetMenuValue).toHaveBeenCalledTimes(1)
		expect(mockSetMenuValue).toHaveBeenCalledWith('items')
	})
})
