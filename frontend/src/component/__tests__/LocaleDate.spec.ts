import LocaleDate from '@/component/LocaleDate.vue'
import { vuetify } from '@/main'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('LocaleDate', async () => {
	it('renders null properly', async () => {
		const wrapper = mount(LocaleDate, {
			global: { plugins: [vuetify] },
			props: { stat: null }
		})

		expect(wrapper.html()).toEqual('–')
	})

	it('renders undefined properly', async () => {
		const wrapper = mount(LocaleDate, {
			global: { plugins: [vuetify] },
			props: { stat: undefined }
		})

		expect(wrapper.html()).toEqual('–')
	})

	it('renders Date properly', async () => {
		const wrapper = mount(LocaleDate, {
			global: { plugins: [vuetify] },
			props: { stat: new Date('2021-12-31') }
		})

		expect(wrapper.html()).toEqual('31.12.2021')
	})

	it('renders string properly', async () => {
		const wrapper = mount(LocaleDate, {
			global: { plugins: [vuetify] },
			props: { stat: '2004-05-03T00:00:00' }
		})

		expect(wrapper.html()).toEqual('3.5.2004')
	})
})
