import { ResizeObserverMock } from '@/__tests__/global-mocks'
import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import vuetify from '@/plugin/vuetify'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiStore: (): WikibasePageStoreType => ({
		...mockWikiStore,
		wikibasePage: { ...mockWikiStore.wikibasePage, errorState: true }
	})
}))

describe('WikibaseTableContainer', async () => {
	it('renders error properly', async () => {
		const wrapper = mount(WikibaseTableContainer, { global: { plugins: [vuetify] } })

		const tableContainer = wrapper.find('div.wikibase-table-container')
		expect(tableContainer.exists()).toEqual(true)

		const typeFilter = tableContainer.find('div.wikibase-type-filter')
		expect(typeFilter.exists()).toEqual(true)

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(true)
		expect(alert.classes()).toContain('text-error')

		const alertTitle = alert.find('div.v-alert-title')
		expect(alertTitle.exists()).toEqual(true)
		expect(alertTitle.text()).toEqual('Error')

		expect(alert.text()).toContain('Error fetching data')

		const table = tableContainer.find('div.wikibase-table')
		expect(table.exists()).toEqual(true)
	})
})
