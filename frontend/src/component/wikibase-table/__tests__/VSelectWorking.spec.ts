import VSelectWorking from '@/component/wikibase-table/VSelectWorking.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const mockOnChange = vi.fn().mockName('OnChange')

describe('VSelectWorking', async () => {
	beforeEach(() => vi.resetAllMocks())

	it(`renders properly`, async () => {
		const wrapper = mount(VSelectWorking, {
			global: { plugins: [vuetify] },
			props: { onChange: mockOnChange }
		})

		const container = wrapper.find('div.v-input')
		expect(container.exists()).toEqual(true)
	})

	it.todo('updates on value change')
})
