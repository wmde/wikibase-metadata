import WikibaseItem from '@/component/wikibase-item-list/WikibaseItem.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

const { mockCreateDataFetcher, MockDataFetcher } = vi.hoisted(() => ({
	mockCreateDataFetcher: vi.fn().mockName('DataFetcher'),
	MockDataFetcher: vi.fn(
		class {
			data
			loading
			status
			constructor(actionApiUrl: string | null) {
				mockCreateDataFetcher(actionApiUrl)
				this.data = { value: null }
				this.loading = { value: null }
				this.status = { value: null }
			}
		}
	)
}))

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
})
