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
					urls: {
						baseUrl: 'https://asdf.test',
						scriptPath: 'script'
					}
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
					urls: {
						baseUrl: 'https://asdf.test',
						scriptPath: null
					}
				}
			}
		})

		expect(mockCreateDataFetcher).toHaveBeenCalledTimes(1)
		expect(mockCreateDataFetcher).toHaveBeenCalledWith(null)
	})

	it(`renders properly without scriptPath`, async () => {
		const wrapper = mount(WikibaseItem, {
			global: { plugins: [vuetify] },
			props: {
				searchValue: '',
				wiki: {
					id: '-1',
					title: "Ahistorical Salutation Department of Figaro's",
					urls: {
						baseUrl: 'https://asdf.test',
						scriptPath: null
					}
				}
			}
		})

		const wiki = wrapper.find('div.wikibase-item')
		expect(wiki.exists()).toEqual(true)
		const title = wiki.find('h4')
		expect(title.exists()).toEqual(true)
		expect(title.text()).toEqual("(-1) Ahistorical Salutation Department of Figaro's")
		const link = wiki.find('a')
		expect(link.attributes()).not.toHaveProperty('href')
		expect(link.text()).toEqual('Action API')
	})
})
