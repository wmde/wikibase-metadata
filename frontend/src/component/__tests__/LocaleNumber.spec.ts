import LocaleNumber from '@/component/LocaleNumber.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('LocaleNumber', async () => {
	it('renders null properly', async () => {
		const wrapper = mount(LocaleNumber, { global: { plugins: [vuetify] }, props: { stat: null } })

		expect(wrapper.html()).toEqual('–')
	})

	it('renders undefined properly', async () => {
		const wrapper = mount(LocaleNumber, {
			global: { plugins: [vuetify] },
			props: { stat: undefined }
		})

		expect(wrapper.html()).toEqual('–')
	})

	it('renders number properly', async () => {
		const wrapper = mount(LocaleNumber, { global: { plugins: [vuetify] }, props: { stat: 14 } })

		expect(wrapper.html()).toEqual('14')
	})

	it('renders large number properly', async () => {
		const wrapper = mount(LocaleNumber, {
			global: { plugins: [vuetify] },
			props: { stat: 10000000 }
		})

		expect(wrapper.html()).toEqual('10.000.000')
	})

	it('renders small number properly', async () => {
		const wrapper = mount(LocaleNumber, { global: { plugins: [vuetify] }, props: { stat: 0.03 } })

		expect(wrapper.html()).toEqual('0,03')
	})
})
