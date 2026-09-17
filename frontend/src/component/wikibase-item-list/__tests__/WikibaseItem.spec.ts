import WikibaseItem from '@/component/wikibase-item-list/WikibaseItem.vue'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseItem', async () => {
	it(`renders $arg properly`, async () => {
		const wrapper = mount(WikibaseItem, {
			global: { plugins: [vuetify] },
			props: {
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
		const title = wiki.find('h4')
		expect(title.exists()).toEqual(true)
		expect(title.text()).toEqual("(-1) Ahistorical Salutation Department of Figaro's")
		const link = wiki.find('a')
		expect(link.attributes()).toHaveProperty('href', 'https://asdf.test/script/api.php')
		expect(link.text()).toEqual('Action API')
	})
})
