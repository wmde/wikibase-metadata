import { ResizeObserverMock } from '@/__tests__/global-mocks'
import App from '@/App.vue'
import vuetify from '@/plugin/vuetify'
import mockMenuStore from '@/stores/__tests__/mock-menu-store'
import mockWikiListStore from '@/stores/__tests__/mock-wikibase-list-store'
import mockWikiPageStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { MenuStoreType } from '@/stores/menu-store'
import type { WikibaseListStoreType } from '@/stores/wikibase-list-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

vi.mock('@/stores/menu-store', () => ({ useMenuStore: (): MenuStoreType => mockMenuStore }))
vi.mock('@/stores/wikibase-list-store', () => ({
	useWikiListStore: (): WikibaseListStoreType => mockWikiListStore
}))
vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiPageStore: (): WikibasePageStoreType => mockWikiPageStore
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
