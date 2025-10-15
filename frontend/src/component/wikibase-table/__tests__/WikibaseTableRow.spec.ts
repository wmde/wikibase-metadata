import WikibaseTableRow from '@/component/wikibase-table/WikibaseTableRow.vue'
import { WikibaseType } from '@/graphql/types'
import { vuetify } from '@/main'
import mockSingleWikiStore from '@/stores/__tests__/mock-wikibase-store'
import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

vi.stubGlobal('visualViewport', new EventTarget())

describe('WikibaseTableRow', async () => {
	it('renders properly with minimal info', async () => {
		const wrapper = mount(WikibaseTableRow, {
			global: { plugins: [vuetify] },
			props: {
				wikibase: {
					id: '297',
					title: 'Test Wikibase',
					urls: { baseUrl: 'wikibase.test' },
					quantityObservations: {},
					recentChangesObservations: {}
				}
			}
		})

		const row = wrapper.find('tr')
		expect(row.exists()).toEqual(true)

		expect(row.findAll('td').length).toEqual(5)
		expect(row.findAll('td').map((td) => td.text())).toEqual([
			'',
			'Test Wikibase',
			'wikibase.test',
			'–',
			'–'
		])
	})

	it('renders properly with more info', async () => {
		const wrapper = mount(WikibaseTableRow, {
			global: { plugins: [vuetify] },
			props: {
				wikibase: {
					id: '82',
					wikibaseType: WikibaseType.Cloud,
					title: 'Test Cloud Wikibase',
					urls: { baseUrl: 'wikibase.test' },
					quantityObservations: { mostRecent: { totalTriples: 1 } },
					recentChangesObservations: { mostRecent: { botChangeCount: 2, humanChangeCount: 3 } }
				}
			}
		})

		const row = wrapper.find('tr')
		expect(row.exists()).toEqual(true)

		expect(row.findAll('td').length).toEqual(5)
		expect(row.findAll('td').map((td) => td.text())).toEqual([
			'CLOUD',
			'Test Cloud Wikibase',
			'wikibase.test',
			'1',
			'5'
		])
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
				}
			}
		})

		const row = wrapper.find('tr')
		expect(row.exists()).toEqual(true)

		expect(wrapper.html()).not.toContain('<!--teleport start-->')
		expect(wrapper.html()).not.toContain('<!--teleport end-->')
		expect(document.querySelector('.wikibase-detail-dialog')).toBeNull()

		await row.trigger('click')

		expect(wrapper.html()).toContain('<!--teleport start-->')
		expect(wrapper.html()).toContain('<!--teleport end-->')
		expect(document.querySelector('.wikibase-detail-dialog')).not.toBeNull()
		expect(
			document.querySelector('.wikibase-detail-dialog')?.querySelector('div.wikibase-detail-card')
		).not.toBeNull()
	})
})
