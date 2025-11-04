import { ResizeObserverMock } from '@/__tests__/global-mocks'
import App from '@/App.vue'
import vuetify from '@/plugin/vuetify'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiStore: (): WikibasePageStoreType => mockWikiStore
}))

describe('App', async () => {
	it('mounts renders properly', async () => {
		const wrapper = mount(App, { global: { plugins: [vuetify] } })

		const applicationWrapper = wrapper.find('div.suite-scraper-app')
		expect(applicationWrapper.exists()).toEqual(true)

		const header = applicationWrapper.find('div.header')
		expect(header.exists()).toEqual(true)

		const tableContainer = applicationWrapper.find('div.wikibase-table-container')
		expect(tableContainer.exists()).toEqual(true)
	})
})
