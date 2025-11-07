import WikibaseDetailCardContainer from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCardContainer.vue'
import vuetify from '@/plugin/vuetify'
import mockSingleWikiStore from '@/stores/__tests__/mock-wikibase-store'
import type { WikibaseStoreType } from '@/stores/wikibase-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

vi.stubGlobal('visualViewport', new EventTarget())

const mockSearchWikibase = vi.fn().mockName('searchWikibase')

vi.mock('@/stores/wikibase-store', () => ({
	useSingleWikiStore: (): WikibaseStoreType => ({
		...mockSingleWikiStore,
		searchWikibase: mockSearchWikibase
	})
}))

describe('WikibaseDetailCardContainer', async () => {
	it('renders properly', async () => {
		const wrapper = mount(WikibaseDetailCardContainer, {
			global: { plugins: [vuetify] },
			props: { wikibaseId: 1 }
		})

		const beforeTooltip = document.querySelector('.wikibase-detail-dialog')
		expect(beforeTooltip).toBeNull()

		expect(mockSearchWikibase).toHaveBeenCalledTimes(0)

		const button = wrapper.find('button.v-btn')
		expect(button.exists()).toEqual(true)
		expect(button.classes()).toContain('v-btn--density-comfortable')
		expect(button.text()).toEqual('VIEW')

		await button.trigger('click')
		await nextTick()

		expect(mockSearchWikibase).toHaveBeenCalledTimes(1)
		expect(mockSearchWikibase).toHaveBeenCalledWith(1)

		const afterTooltip = document.querySelector('.wikibase-detail-dialog')
		expect(afterTooltip).not.toBeNull()
	})
})
