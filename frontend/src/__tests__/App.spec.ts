import { describe, expect, it } from 'vitest'

import App from '@/App.vue'
import { mount } from '@vue/test-utils'

describe('App', () => {
	it('mounts renders properly', () => {
		const wrapper = mount(App)
		expect(wrapper.text()).toContain('You did it!')
	})
})
