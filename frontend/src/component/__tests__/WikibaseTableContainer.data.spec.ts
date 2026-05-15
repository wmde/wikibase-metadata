import { ResizeObserverMock } from '@/__tests__/global-mocks'
import WikibaseTableContainer from '@/component/WikibaseTableContainer.vue'
import vuetify from '@/plugin/vuetify'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import testWikibases from '../wikibase-table/__tests__/test-wikibases'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

const { mockFetchWikibasePage } = vi.hoisted(() => ({
	mockFetchWikibasePage: vi.fn().mockName('fetchWikibasePage')
}))

vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiStore: (): WikibasePageStoreType => ({
		...mockWikiStore,
		fetchWikibasePage: mockFetchWikibasePage,
		wikibasePage: {
			...mockWikiStore.wikibasePage,
			data: {
				data: testWikibases.slice(2),
				meta: { totalCount: testWikibases.length, totalPages: Math.ceil(testWikibases.length / 3) }
			}
		}
	})
}))

describe('WikibaseTableContainer', async () => {
	beforeEach(() => setActivePinia(createPinia()))

	it('renders properly', async () => {
		const wrapper = mount(WikibaseTableContainer, { global: { plugins: [vuetify] } })

		const tableContainer = wrapper.find('div.wikibase-table-container')
		expect(tableContainer.exists()).toEqual(true)

		const alert = wrapper.find('div.v-alert')
		expect(alert.exists()).toEqual(false)

		const showing = wrapper.find('div.show-count')
		expect(showing.exists()).toEqual(true)
		expect(showing.text()).toEqual('Showing 3 of 5 instances')

		const table = tableContainer.find('div.wikibase-table')
		expect(table.exists()).toEqual(true)
	})
})
