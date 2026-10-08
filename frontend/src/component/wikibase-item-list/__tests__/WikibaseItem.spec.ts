import WikibaseItem from '@/component/wikibase-item-list/WikibaseItem.vue'
import vuetify from '@/plugin/vuetify'
import type { SearchResult } from '@/util/fetch-data'
import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ref, type Ref } from 'vue'

const { mockCreateDataFetcher, mockDataValue, mockLoadingValue, MockDataFetcher } = vi.hoisted(
	() => ({
		mockCreateDataFetcher: vi.fn().mockName('DataFetcher'),
		mockDataValue: vi.fn().mockName(''),
		mockLoadingValue: vi.fn().mockName(''),
		MockDataFetcher: vi.fn(
			class {
				data: Ref<SearchResult | undefined>
				loading: Ref<boolean>
				status
				constructor(actionApiUrl: string | null) {
					mockCreateDataFetcher(actionApiUrl)
					this.data = ref(mockDataValue())
					this.loading = ref(mockLoadingValue())
					this.status = { value: null }
				}
			}
		)
	})
)

vi.mock('@/util/fetch-data', () => ({ default: MockDataFetcher }))

describe('WikibaseItem', async () => {
	beforeEach(() => vi.resetAllMocks())

	it('creates DataFetcher with scriptPath', async () => {
		expect(mockCreateDataFetcher).toHaveBeenCalledTimes(0)

		mount(WikibaseItem, {
			global: { plugins: [vuetify] },
			props: {
				searchValue: '',
				wiki: {
					id: '-1',
					title: "Ahistorical Salutation Department of Figaro's",
					urls: { baseUrl: 'https://asdf.test', scriptPath: 'script' }
				}
			}
		})

		expect(mockCreateDataFetcher).toHaveBeenCalledTimes(1)
		expect(mockCreateDataFetcher).toHaveBeenCalledWith('https://asdf.test/script/api.php')
	})

	it('creates DataFetcher without scriptPath', async () => {
		expect(mockCreateDataFetcher).toHaveBeenCalledTimes(0)

		mount(WikibaseItem, {
			global: { plugins: [vuetify] },
			props: {
				searchValue: '',
				wiki: {
					id: '-1',
					title: "Ahistorical Salutation Department of Figaro's",
					urls: { baseUrl: 'https://asdf.test', scriptPath: null }
				}
			}
		})

		expect(mockCreateDataFetcher).toHaveBeenCalledTimes(1)
		expect(mockCreateDataFetcher).toHaveBeenCalledWith(null)
	})

	it('renders properly with no searchValue', async () => {
		mockDataValue.mockReturnValueOnce(null)
		mockLoadingValue.mockReturnValueOnce(false)

		const wrapper = mount(WikibaseItem, {
			global: { plugins: [vuetify] },
			props: {
				searchValue: '',
				wiki: {
					id: '-1',
					title: "Ahistorical Salutation Department of Figaro's",
					urls: { baseUrl: 'https://asdf.test', scriptPath: 'script' }
				}
			}
		})

		const wiki = wrapper.find('div.wikibase-item')
		expect(wiki.exists()).toEqual(true)

		const headerContainer = wiki.find('div.header-container')
		expect(headerContainer.exists()).toEqual(true)

		const title = headerContainer.find('div.wiki-title')
		expect(title.exists()).toEqual(true)
		expect(title.text()).toEqual("Ahistorical Salutation Department of Figaro's")

		const status = headerContainer.find('div.status')
		expect(status.exists()).toEqual(true)
		expect(status.text()).not.toEqual('Loading')
	})

	it('renders properly with loading', async () => {
		mockDataValue.mockReturnValueOnce(null)
		mockLoadingValue.mockReturnValueOnce(true)

		const wrapper = mount(WikibaseItem, {
			global: { plugins: [vuetify] },
			props: {
				searchValue: 'search',
				wiki: {
					id: '-1',
					title: "Ahistorical Salutation Department of Figaro's",
					urls: { baseUrl: 'https://asdf.test', scriptPath: 'script' }
				}
			}
		})

		const wiki = wrapper.find('div.wikibase-item')
		expect(wiki.exists()).toEqual(true)

		const headerContainer = wiki.find('div.header-container')
		expect(headerContainer.exists()).toEqual(true)

		const title = headerContainer.find('div.wiki-title')
		expect(title.exists()).toEqual(true)
		expect(title.text()).toEqual("Ahistorical Salutation Department of Figaro's")

		const status = headerContainer.find('div.status')
		expect(status.exists()).toEqual(true)
		expect(status.text()).toEqual('Loading')
	})

	it('renders properly with data', async () => {
		const data: SearchResult = {
			searchInfo: {
				search: 'search'
			},
			success: 1,
			search: [
				{
					id: '11',
					title: 'Search',
					pageid: 1,
					repository: 'https://asdf.text',
					url: 'https://asdf.text/w/Q11',
					concepturi: 'https://asdf.text/w/Q11',
					label: 'Search',
					description: 'A search implementation',
					match: {
						type: 'item',
						language: 'en',
						text: 'SearchLabel'
					}
				},
				{
					id: '12',
					title: 'Search Result',
					pageid: 1,
					repository: 'https://asdf.text',
					url: 'https://asdf.text/w/Q12',
					concepturi: 'https://asdf.text/w/Q12',
					label: 'Search Result',
					description: 'Something that is returned by a search',
					match: {
						type: 'item',
						language: 'en',
						text: 'SearchResultLabel'
					}
				}
			]
		}
		mockDataValue.mockReturnValueOnce(data)
		mockLoadingValue.mockReturnValueOnce(false)

		const wrapper = mount(WikibaseItem, {
			global: { plugins: [vuetify] },
			props: {
				searchValue: 'search',
				wiki: {
					id: '-1',
					title: "Ahistorical Salutation Department of Figaro's",
					urls: { baseUrl: 'https://asdf.test', scriptPath: 'script' }
				}
			}
		})

		const wiki = wrapper.find('div.wikibase-item')
		expect(wiki.exists()).toEqual(true)

		const headerContainer = wiki.find('div.header-container')
		expect(headerContainer.exists()).toEqual(true)

		const title = headerContainer.find('div.wiki-title')
		expect(title.exists()).toEqual(true)
		expect(title.text()).toEqual("Ahistorical Salutation Department of Figaro's")

		const resultsContainer = wiki.find('div.results-container')
		expect(resultsContainer.exists()).toEqual(true)

		const results = resultsContainer.findAll('div.result')
		expect(results).toHaveLength(2)

		const resultOne = resultsContainer.findAll('div.result')[0]

		const labelContainerOne = resultOne.find('div.item-label-container')
		expect(labelContainerOne.exists()).toEqual(true)

		const labelOne = labelContainerOne.find('div.item-label')
		expect(labelOne.exists()).toEqual(true)
		const linkOne = labelOne.find('a')
		expect(linkOne.exists()).toEqual(true)
		expect(linkOne.attributes()).toHaveProperty('href', 'https://asdf.text/w/Q11')
		expect(linkOne.attributes()).toHaveProperty('target', '_blank')
		expect(linkOne.text()).toEqual('Search')

		const idContainerOne = labelContainerOne.find('div.item-id')
		expect(idContainerOne.exists()).toEqual(true)
		expect(idContainerOne.text()).toEqual('11')

		const descriptionOne = resultOne.find('div.description')
		expect(descriptionOne.exists()).toEqual(true)
		expect(descriptionOne.text()).toEqual('A search implementation')

		const resultTwo = resultsContainer.findAll('div.result')[1]

		const labelContainerTwo = resultTwo.find('div.item-label-container')
		expect(labelContainerTwo.exists()).toEqual(true)

		const labelTwo = labelContainerTwo.find('div.item-label')
		const linkTwo = labelTwo.find('a')
		expect(linkTwo.attributes()).toHaveProperty('href', 'https://asdf.text/w/Q12')
		expect(linkTwo.text()).toEqual('Search Result')

		const idContainerTwo = labelContainerTwo.find('div.item-id')
		expect(idContainerTwo.text()).toEqual('12')

		const descriptionTwo = resultTwo.find('div.description')
		expect(descriptionTwo.text()).toEqual('Something that is returned by a search')
	})

	it('renders properly with search value and no data, loading', async () => {
		mockDataValue.mockReturnValueOnce(null)
		mockLoadingValue.mockReturnValueOnce(false)

		const wrapper = mount(WikibaseItem, {
			global: { plugins: [vuetify] },
			props: {
				searchValue: 'search',
				wiki: {
					id: '-1',
					title: "Ahistorical Salutation Department of Figaro's",
					urls: { baseUrl: 'https://asdf.test', scriptPath: 'script' }
				}
			}
		})

		const wiki = wrapper.find('div.wikibase-item')
		expect(wiki.exists()).toEqual(false)
	})
})
