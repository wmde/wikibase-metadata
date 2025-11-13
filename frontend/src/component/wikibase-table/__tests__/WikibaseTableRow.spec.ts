import WikibaseTableRow from '@/component/wikibase-table/WikibaseTableRow.vue'
import { WikibaseCategory, WikibaseType } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import mockSingleWikiStore from '@/stores/__tests__/mock-wikibase-store'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.stubGlobal('visualViewport', new EventTarget())

describe('WikibaseTableRow', async () => {
	beforeEach(() => setActivePinia(createPinia()))

	it('renders properly with minimal info', async () => {
		const wrapper = mount(WikibaseTableRow, {
			global: { plugins: [vuetify] },
			props: {
				wikibase: {
					id: '297',
					title: 'Test Wikibase',
					urls: { baseUrl: 'wikibase.test' },
					quantityObservations: {},
					recentChangesObservations: {},
					wikibaseType: WikibaseType.Unknown
				},
				index: 2
			}
		})

		const row = wrapper.find('tr')
		expect(row.exists()).toEqual(true)

		expect(row.findAll('td').length).toEqual(8)
		expect(row.findAll('td').map((td) => td.text())).toEqual([
			'3',
			'Unknown',
			'Test Wikibase',
			'–',
			'–',
			'–',
			'–',
			'VIEW'
		])
		expect(row.findAll('td')[2]?.find('a').exists()).toEqual(true)
		expect(row.findAll('td')[2]?.find('a').attributes()).toHaveProperty('href', 'wikibase.test')
	})

	it('renders properly with more info', async () => {
		const wrapper = mount(WikibaseTableRow, {
			global: { plugins: [vuetify] },
			props: {
				wikibase: {
					id: '82',
					wikibaseType: WikibaseType.Cloud,
					title: 'Test Cloud Wikibase',
					description: 'BEHOLD! A test Wikibase!',
					category: WikibaseCategory.ExperimentalAndPrototypeProjects,
					urls: { baseUrl: 'wikibase.test' },
					quantityObservations: { mostRecent: { totalTriples: 1 } },
					recentChangesObservations: { mostRecent: { botChangeCount: 2, humanChangeCount: 3 } }
				},
				index: 3
			}
		})

		const row = wrapper.find('tr')
		expect(row.exists()).toEqual(true)

		expect(row.findAll('td').length).toEqual(8)
		expect(row.findAll('td').map((td) => td.text())).toEqual([
			'4',
			'Wikibase Cloud',
			'Test Cloud Wikibase',
			'1',
			'5',
			'Experimental & Prototype Projects',
			'BEHOLD! A test Wikibase!',
			'VIEW'
		])
		expect(row.findAll('td')[2]?.find('a').exists()).toEqual(true)
		expect(row.findAll('td')[2]?.find('a').attributes()).toHaveProperty('href', 'wikibase.test')
	})

	it('triggers dialog on click', async () => {
		const wrapper = mount(WikibaseTableRow, {
			global: { mocks: { useSingleWikiStore: () => mockSingleWikiStore }, plugins: [vuetify] },
			props: {
				wikibase: {
					id: '82',
					wikibaseType: WikibaseType.Cloud,
					title: 'Test Cloud Wikibase',
					urls: { baseUrl: 'wikibase.test' },
					quantityObservations: { mostRecent: { totalTriples: 1 } },
					recentChangesObservations: { mostRecent: { botChangeCount: 2, humanChangeCount: 3 } }
				},
				index: 4
			}
		})

		const row = wrapper.find('tr')
		expect(row.exists()).toEqual(true)

		const button = row.find('button.v-btn')
		expect(button.exists()).toEqual(true)

		expect(wrapper.html()).not.toContain('<!--teleport start-->')
		expect(wrapper.html()).not.toContain('<!--teleport end-->')
		expect(document.querySelector('.wikibase-detail-dialog')).toBeNull()

		await button.trigger('click')

		expect(wrapper.html()).toContain('<!--teleport start-->')
		expect(wrapper.html()).toContain('<!--teleport end-->')
		expect(document.querySelector('.wikibase-detail-dialog')).not.toBeNull()
		expect(
			document.querySelector('.wikibase-detail-dialog')?.querySelector('div.wikibase-detail-card')
		).not.toBeNull()
	})
})
