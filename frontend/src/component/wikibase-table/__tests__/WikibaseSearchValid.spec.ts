import WikibaseSearchValid from '@/component/wikibase-table/WikibaseSearchValid.vue'
import vuetify from '@/plugin/vuetify'
import mockSearchStore from '@/stores/__tests__/mock-search-store'
import mockWikiPageStore from '@/stores/__tests__/mock-wikibase-page-store'
import type { SearchStoreType } from '@/stores/search-store'
import type { WikibasePageStoreType } from '@/stores/wikibase-page-store'
import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const { mockDataValue, mockLoadingValue, mockMenuValue, mockSearchValue } = vi.hoisted(() => ({
	mockDataValue: vi.fn().mockName('data'),
	mockLoadingValue: vi.fn().mockName('loading'),
	mockMenuValue: vi.fn().mockName('menuValue'),
	mockSearchValue: vi.fn().mockName('searchValue')
}))
vi.mock('@/stores/search-store', () => ({
	useSearchStore: (): SearchStoreType => ({
		...mockSearchStore,
		menuValue: mockMenuValue(),
		searchValue: mockSearchValue()
	})
}))
vi.mock('@/stores/wikibase-page-store', () => ({
	useWikiPageStore: (): WikibasePageStoreType => ({
		...mockWikiPageStore,
		wikibasePage: {
			...mockWikiPageStore.wikibasePage,
			data: mockDataValue(),
			loading: mockLoadingValue()
		}
	})
}))

describe('WikibaseSearchValid', async () => {
	beforeEach(() => vi.resetAllMocks())

	describe('instances', async () => {
		it('renders properly with no search value', async () => {
			mockDataValue.mockReturnValueOnce(undefined)
			mockLoadingValue.mockReturnValueOnce(true)
			mockMenuValue.mockReturnValueOnce('instances')
			mockSearchValue.mockReturnValueOnce('')

			const wrapper = mount(WikibaseSearchValid, { global: { plugins: [vuetify] } })

			const container = wrapper.find('label.search-error')
			expect(container.exists()).toEqual(true)

			const results = container.findAll('div')
			expect(results).toHaveLength(0)
		})

		it('renders properly with disallowed search value', async () => {
			mockDataValue.mockReturnValueOnce(undefined)
			mockLoadingValue.mockReturnValueOnce(true)
			mockMenuValue.mockReturnValueOnce('instances')
			mockSearchValue.mockReturnValueOnce('a$df')

			const wrapper = mount(WikibaseSearchValid, { global: { plugins: [vuetify] } })

			const container = wrapper.find('label.search-error')
			expect(container.exists()).toEqual(true)

			const results = container.findAll('div')
			expect(results).toHaveLength(1)
			expect(results[0].text()).toEqual('Disallowed Characters')
		})

		it('renders properly with undefined data', async () => {
			mockDataValue.mockReturnValueOnce(undefined)
			mockLoadingValue.mockReturnValueOnce(false)
			mockMenuValue.mockReturnValueOnce('instances')
			mockSearchValue.mockReturnValueOnce('asdf')

			const wrapper = mount(WikibaseSearchValid, { global: { plugins: [vuetify] } })

			const container = wrapper.find('label.search-error')
			expect(container.exists()).toEqual(true)

			const results = container.findAll('div')
			expect(results).toHaveLength(1)
			expect(results[0].text()).toEqual(
				'No results for "asdf" — try a different keyword or category'
			)
		})

		it('renders properly with no data', async () => {
			mockDataValue.mockReturnValueOnce({
				data: [],
				meta: { totalCount: 0, totalPages: 0, totalEdits: 0, totalTriples: 0 }
			})
			mockLoadingValue.mockReturnValueOnce(false)
			mockMenuValue.mockReturnValueOnce('instances')
			mockSearchValue.mockReturnValueOnce('asdf')

			const wrapper = mount(WikibaseSearchValid, { global: { plugins: [vuetify] } })

			const container = wrapper.find('label.search-error')
			expect(container.exists()).toEqual(true)

			const results = container.findAll('div')
			expect(results).toHaveLength(1)
			expect(results[0].text()).toEqual(
				'No results for "asdf" — try a different keyword or category'
			)
		})
	})

	describe('items', async () => {
		it('renders properly with no search value', async () => {
			mockLoadingValue.mockReturnValueOnce(true)
			mockMenuValue.mockReturnValueOnce('items')
			mockSearchValue.mockReturnValueOnce('')

			const wrapper = mount(WikibaseSearchValid, { global: { plugins: [vuetify] } })

			const container = wrapper.find('label.search-error')
			expect(container.exists()).toEqual(true)

			const results = container.findAll('div')
			expect(results).toHaveLength(0)
		})

		it('renders properly with disallowed search value', async () => {
			mockLoadingValue.mockReturnValueOnce(true)
			mockMenuValue.mockReturnValueOnce('items')
			mockSearchValue.mockReturnValueOnce('a$df')

			const wrapper = mount(WikibaseSearchValid, { global: { plugins: [vuetify] } })

			const container = wrapper.find('label.search-error')
			expect(container.exists()).toEqual(true)

			const results = container.findAll('div')
			expect(results).toHaveLength(0)
		})

		it('renders properly with no results', async () => {
			mockLoadingValue.mockReturnValueOnce(false)
			mockMenuValue.mockReturnValueOnce('items')
			mockSearchValue.mockReturnValueOnce('asdf')

			const wrapper = mount(WikibaseSearchValid, { global: { plugins: [vuetify] } })

			const container = wrapper.find('label.search-error')
			expect(container.exists()).toEqual(true)

			const results = container.findAll('div')
			expect(results).toHaveLength(0)
		})
	})
})
