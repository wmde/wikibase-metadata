import vuetify from '@/plugin/vuetify'
import mockWikiListStore from '@/stores/__tests__/mock-wikibase-list-store'
import type { WikibaseListStoreType } from '@/stores/wikibase-list-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'
import WikibaseItemList from '../WikibaseItemList.vue'

vi.mock('@/stores/wikibase-list-store', () => ({
	useWikiListStore: (): WikibaseListStoreType => ({
		...mockWikiListStore,
		wikibaseList: { ...mockWikiListStore.wikibaseList, loading: true }
	})
}))

describe('WikibaseItemList', async () => {
	it(`renders loading properly`, async () => {
		const wrapper = mount(WikibaseItemList, { global: { plugins: [vuetify] } })

		expect(wrapper.text()).toEqual('Loading')
	})
})
