import LocaleNumber from '@/component/LocaleNumber.vue'
import { vuetify } from '@/main'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import 'vuetify/styles'

describe('LocaleNumber', () => {
	it('renders null properly', () => {
		const wrapper = mount(LocaleNumber, {
			global: { plugins: [vuetify] },
			props: { stat: null }
		})

		expect(wrapper.html()).toEqual('–')
	})

	it('renders undefined properly', () => {
		const wrapper = mount(LocaleNumber, {
			global: { plugins: [vuetify] },
			props: { stat: undefined }
		})

		expect(wrapper.html()).toEqual('–')
	})

	it('renders number properly', () => {
		const wrapper = mount(LocaleNumber, {
			global: { plugins: [vuetify] },
			props: { stat: 14 }
		})

		expect(wrapper.html()).toEqual('14')
	})

	it('renders large number properly', () => {
		const wrapper = mount(LocaleNumber, {
			global: { plugins: [vuetify] },
			props: { stat: 10000000 }
		})

		expect(wrapper.html()).toEqual('10.000.000')
	})

	it('renders small number properly', () => {
		const wrapper = mount(LocaleNumber, {
			global: { plugins: [vuetify] },
			props: { stat: 0.03 }
		})

		expect(wrapper.html()).toEqual('0,03')
	})
})
