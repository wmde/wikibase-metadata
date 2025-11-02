import WikibaseTypeFilter from '@/component/wikibase-table/WikibaseTypeFilter.vue'
import { WikibaseType, type WbFragment } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import mockWikiStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.stubGlobal('visualViewport', new EventTarget())

const testWikibasesAlt: WbFragment[] = [
	{
		id: '1',
		title: 'Test Wikibase',
		urls: { baseUrl: 'test-wikibase-001.test' },
		quantityObservations: {},
		recentChangesObservations: {},
		wikibaseType: WikibaseType.Other
	},
	{
		id: '2',
		title: 'Test Wikibase #2',
		urls: { baseUrl: 'test-wikibase-002.test' },
		quantityObservations: { mostRecent: { totalTriples: 14 } },
		recentChangesObservations: {},
		wikibaseType: WikibaseType.Suite
	},
	{
		id: '3',
		title: 'Test Wikibase #3',
		urls: { baseUrl: 'test-wikibase-003.test' },
		quantityObservations: { mostRecent: { totalTriples: 1 } },
		recentChangesObservations: { mostRecent: { botChangeCount: 100 } },
		wikibaseType: WikibaseType.Other
	},
	{
		id: '4',
		title: 'Test Wikibase #4',
		urls: { baseUrl: 'test-wikibase-004.test' },
		quantityObservations: { mostRecent: {} },
		recentChangesObservations: { mostRecent: { humanChangeCount: 31 } },
		wikibaseType: WikibaseType.Suite
	},
	{
		id: '5',
		title: 'Test Wikibase #5',
		urls: { baseUrl: 'test-wikibase-005.test' },
		quantityObservations: { mostRecent: { totalTriples: 300 } },
		recentChangesObservations: { mostRecent: { humanChangeCount: 31, botChangeCount: 69 } },
		wikibaseType: WikibaseType.Unknown
	}
]

vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiStore: (): WikibasePageStoreType => ({
		...mockWikiStore,
		wikibaseFilter: { wikibaseType: { exclude: [WikibaseType.Cloud, WikibaseType.Test] } },
		wikibasePage: {
			...mockWikiStore.wikibasePage,
			data: { meta: { totalCount: 5 }, data: testWikibasesAlt }
		}
	})
}))

describe('WikibaseTypeFilter', async () => {
	beforeEach(() => setActivePinia(createPinia()))

	it('renders properly', async () => {
		const wrapper = mount(WikibaseTypeFilter, {
			global: { plugins: [vuetify] }
		})

		const selectContainer = wrapper.find('div.wikibase-type-filter')
		expect(selectContainer.exists()).toEqual(true)
		expect(selectContainer.classes()).toContain('v-select')
		expect(selectContainer.classes()).toContain('v-select--chips')
		expect(selectContainer.classes()).toContain('v-select--multiple')

		const label = selectContainer.find('label.v-label')
		expect(label.exists()).toEqual(true)
		expect(label.text()).toEqual('Include Wikibase Types')
	})
})
