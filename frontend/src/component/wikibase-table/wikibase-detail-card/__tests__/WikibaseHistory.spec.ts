import WikibaseHistory from '@/component/wikibase-table/wikibase-detail-card/WikibaseHistory.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseHistory', async () => {
	it('renders nothing', async () => {
		const wrapper = mount(WikibaseHistory, {
			global: { plugins: [vuetify] },
			props: {
				obs: {}
			}
		})

		const historyContainer = wrapper.find('.history-container')
		expect(historyContainer.exists()).toEqual(false)
	})

	it('renders label properly', async () => {
		const wrapper = mount(WikibaseHistory, {
			global: { plugins: [vuetify] },
			props: {
				obs: { initiationDate: new Date(2026, 5, 15) }
			}
		})

		const historyContainer = wrapper.find('.history-container')
		expect(historyContainer.exists()).toEqual(true)
		expect(historyContainer.classes()).toContain('v-expansion-panels')
		expect(historyContainer.text()).toEqual('Edit History')
	})

	it('renders label properly ii', async () => {
		const wrapper = mount(WikibaseHistory, {
			global: { plugins: [vuetify] },
			props: {
				obs: { itemDates: [{ id: '1', q: 14, creationDate: new Date(2026, 6, 1) }] }
			}
		})

		const historyContainer = wrapper.find('.history-container')
		expect(historyContainer.exists()).toEqual(true)
		expect(historyContainer.classes()).toContain('v-expansion-panels')
		expect(historyContainer.text()).toEqual('Edit History')
	})

	it.todo('renders internal data properly - requires clicking to open expansion panel')
})
