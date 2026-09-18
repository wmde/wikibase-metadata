import WikibaseItem from '@/component/wikibase-item-list/WikibaseItem.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseItem', async () => {
	it(`renders properly before searching`, async () => {
		const wrapper = mount(WikibaseItem, {
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

		const wiki = wrapper.find('div.wikibase-item')
		expect(wiki.exists()).toEqual(true)
		const title = wiki.find('div.wiki-title')
		expect(title.exists()).toEqual(true)
		expect(title.text()).toEqual("Ahistorical Salutation Department of Figaro's")
	})
})
