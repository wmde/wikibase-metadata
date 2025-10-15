import { ResizeObserverMock } from '@/__tests__/global-mocks'
import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import { vuetify } from '@/main'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

describe('WikibaseTableContainer', async () => {
	it('mounts renders properly', async () => {
		const wrapper = mount(WikibaseTableContainer, {
			global: { mocks: { useWikiStore: () => mockWikiStore }, plugins: [vuetify] }
		})

		const tableContainer = wrapper.find('div.wikibase-table-container')
		expect(tableContainer.exists()).toEqual(true)

		const typeFilter = tableContainer.find('div.wikibase-type-filter')
		expect(typeFilter.exists()).toEqual(true)

		const table = tableContainer.find('div.wikibase-table')
		expect(table.exists()).toEqual(true)
	})
})
