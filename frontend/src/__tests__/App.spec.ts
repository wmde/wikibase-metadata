import { ResizeObserverMock } from '@/__tests__/global-mocks'
import App from '@/App.vue'
import { vuetify } from '@/main'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'
import 'vuetify/styles'

vi.stubGlobal('ResizeObserver', ResizeObserverMock)

describe('App', async () => {
	it('mounts renders properly', async () => {
		const wrapper = mount(App, {
			global: { mocks: { useWikiStore: () => mockWikiStore }, plugins: [vuetify] }
		})

		const applicationWrapper = wrapper.find('div.suite-scraper-app')
		expect(applicationWrapper.exists()).toEqual(true)

		const header = applicationWrapper.find('div.header')
		expect(header.exists()).toEqual(true)

		const tableContainer = applicationWrapper.find('div.wikibase-table-container')
		expect(tableContainer.exists()).toEqual(true)
	})
})
