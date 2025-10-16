import WikibaseTypeFilter from '@/component/wikibase-table/WikibaseTypeFilter.vue'
import { vuetify } from '@/main'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

vi.stubGlobal('visualViewport', new EventTarget())

describe('WikibaseTypeFilter', async () => {
	it('renders properly', async () => {
		const wrapper = mount(WikibaseTypeFilter, {
			global: { mocks: { useWikiStore: () => mockWikiStore }, plugins: [vuetify] }
		})

		const selectContainer = wrapper.find('div.wikibase-type-filter')
		expect(selectContainer.exists()).toEqual(true)
		expect(selectContainer.classes()).toContain('v-select')
		expect(selectContainer.classes()).toContain('v-select--chips')
		expect(selectContainer.classes()).toContain('v-select--multiple')

		const label = selectContainer.find('label.v-label')
		expect(label.exists()).toEqual(true)
		expect(label.text()).toEqual('Exclude Wikibase Types')

		const selection = selectContainer.find('div.v-select__selection')
		expect(selection.exists()).toEqual(true)
		expect(selection.findAll('span.v-chip').length).toEqual(1)
		expect(selection.find('span.v-chip').text()).toEqual('TEST')
	})
})
