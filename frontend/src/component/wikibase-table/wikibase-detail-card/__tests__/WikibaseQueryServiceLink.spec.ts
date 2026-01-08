import WikibaseQueryServiceLink from '@/component/wikibase-table/wikibase-detail-card/WikibaseQueryServiceLink.vue'
import { WikibaseCategory, WikibaseType, type SingleWikibaseFragment } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

const testWiki: SingleWikibaseFragment = {
	id: '1',
	title: 'Test Wikibase',
	category: WikibaseCategory.FictionalAndCreativeWorks,
	description: 'A test description',
	urls: {
		baseUrl: 'https://test-wikibase-001.test',
		sparqlFrontendUrl: 'https://test-wikibase-001.test/query'
	},
	quantityObservations: { allObservations: [] },
	recentChangesObservations: {},
	timeToFirstValueObservations: {},
	wikibaseType: WikibaseType.Cloud
}

describe('WikibaseQueryServiceLink', async () => {
	it('renders Cloud properly', async () => {
		const wrapper = mount(WikibaseQueryServiceLink, {
			global: { plugins: [vuetify] },
			props: { wikibase: { ...testWiki, wikibaseType: WikibaseType.Cloud } }
		})

		// const tooltip = document.querySelector('.sparql-url-tooltip')
		// expect(tooltip).not.toBeNull()
		// expect(tooltip?.textContent).toEqual('Automatically pulled from Cloud API')

		const container = wrapper.find('div.wikibase-url')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-container')

		const link = container.find('a')
		expect(link.exists()).toEqual(true)
		expect(link.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test/query')
		expect(link.text()).toEqual('Query Service')
	})

	it('renders Other properly', async () => {
		const wrapper = mount(WikibaseQueryServiceLink, {
			global: { plugins: [vuetify] },
			props: { wikibase: { ...testWiki, wikibaseType: WikibaseType.Other } }
		})

		// const tooltip = document.querySelector('.sparql-url-tooltip')
		// expect(tooltip).not.toBeNull()
		// expect(tooltip?.textContent).toEqual('Manually set')

		const container = wrapper.find('div.wikibase-url')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-container')

		const link = container.find('a')
		expect(link.exists()).toEqual(true)
		expect(link.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test/query')
		expect(link.text()).toEqual('Query Service')
	})

	it('renders Suite properly', async () => {
		const wrapper = mount(WikibaseQueryServiceLink, {
			global: { plugins: [vuetify] },
			props: { wikibase: { ...testWiki, wikibaseType: WikibaseType.Suite } }
		})

		// const tooltip = document.querySelector('.sparql-url-tooltip')
		// expect(tooltip).not.toBeNull()
		// expect(tooltip?.textContent).toEqual('Manually set')

		const container = wrapper.find('div.wikibase-url')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-container')

		const link = container.find('a')
		expect(link.exists()).toEqual(true)
		expect(link.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test/query')
		expect(link.text()).toEqual('Query Service')
	})

	it('renders Test properly', async () => {
		const wrapper = mount(WikibaseQueryServiceLink, {
			global: { plugins: [vuetify] },
			props: { wikibase: { ...testWiki, wikibaseType: WikibaseType.Test } }
		})

		// const tooltip = document.querySelector('.sparql-url-tooltip')
		// expect(tooltip).not.toBeNull()
		// expect(tooltip?.textContent).toEqual('Manually set')

		const container = wrapper.find('div.wikibase-url')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-container')

		const link = container.find('a')
		expect(link.exists()).toEqual(true)
		expect(link.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test/query')
		expect(link.text()).toEqual('Query Service')
	})

	it('renders Unknown properly', async () => {
		const wrapper = mount(WikibaseQueryServiceLink, {
			global: { plugins: [vuetify] },
			props: { wikibase: { ...testWiki, wikibaseType: WikibaseType.Unknown } }
		})

		// const tooltip = document.querySelector('.sparql-url-tooltip')
		// expect(tooltip).not.toBeNull()
		// expect(tooltip?.textContent).toEqual('Not set')

		const container = wrapper.find('div.wikibase-url')
		expect(container.exists()).toEqual(true)
		expect(container.classes()).toContain('v-container')

		const link = container.find('a')
		expect(link.exists()).toEqual(true)
		expect(link.attributes()).toHaveProperty('href', 'https://test-wikibase-001.test/query')
		expect(link.text()).toEqual('Query Service')
	})
})
