import WikibaseHistoryDetail from '@/component/wikibase-table/wikibase-detail-card/WikibaseHistoryDetail.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseHistoryDetail', async () => {
	it('renders internal data properly', async () => {
		const wrapper = mount(WikibaseHistoryDetail, {
			global: { plugins: [vuetify] },
			props: {
				obs: {
					initiationDate: new Date(2026, 5, 15),
					itemDates: [
						{ id: '-1', q: 1, creationDate: new Date(2026, 5, 16) },
						{ id: '-2', q: 10, creationDate: new Date(2026, 5, 17) }
					]
				}
			}
		})

		const milestoneContainer = wrapper.find('.milestone-container')
		expect(milestoneContainer.exists()).toEqual(true)

		const milestones = milestoneContainer.findAll('div.milestone')
		expect(milestones).toHaveLength(3)

		expect(milestones[0].find('div.milestone-q').text()).toEqual('First Record')
		expect(milestones[0].find('div.milestone-date').text()).toEqual('15.6.2026 00:00:00')

		expect(milestones[1].find('div.milestone-q').text()).toEqual('Q1')
		expect(milestones[1].find('div.milestone-date').text()).toEqual('16.6.2026 00:00:00')

		expect(milestones[2].find('div.milestone-q').text()).toEqual('Q10')
		expect(milestones[2].find('div.milestone-date').text()).toEqual('17.6.2026 00:00:00')
	})
})
