import AccreditedTypeChip from '@/component/wikibase-table/wikibase-detail-card/AccreditedTypeChip.vue'
import { WikibaseCategory, WikibaseType, type SingleWikibaseFragment } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

const testWiki: SingleWikibaseFragment = {
	id: '1',
	title: 'Test Wikibase',
	category: WikibaseCategory.FictionalAndCreativeWorks,
	description: 'A test description',
	urls: { baseUrl: 'https://test-wikibase-001.test' },
	quantityObservations: {},
	recentChangesObservations: {},
	timeToFirstValueObservations: {},
	wikibaseType: WikibaseType.Cloud
}

describe('AccreditedTypeChip', async () => {
	it('renders Cloud properly', async () => {
		const wrapper = mount(AccreditedTypeChip, {
			global: { plugins: [vuetify] },
			props: { wikibase: { ...testWiki, wikibaseType: WikibaseType.Cloud } }
		})

		const tooltip = document.querySelector('.type-tooltip-cloud')
		expect(tooltip).not.toBeNull()
		expect(tooltip?.textContent).toEqual('Automatically pulled from Cloud API')

		const chip = wrapper.find('span.wikibase-type-chip')
		expect(chip.exists()).toEqual(true)
		expect(chip.text()).toEqual('Wikibase Cloud')
	})

	it('renders Other properly', async () => {
		const wrapper = mount(AccreditedTypeChip, {
			global: { plugins: [vuetify] },
			props: { wikibase: { ...testWiki, wikibaseType: WikibaseType.Other } }
		})

		const tooltip = document.querySelector('.type-tooltip-other')
		expect(tooltip).not.toBeNull()
		expect(tooltip?.textContent).toEqual('Manually set')

		const chip = wrapper.find('span.wikibase-type-chip')
		expect(chip.exists()).toEqual(true)
		expect(chip.text()).toEqual('Other')
	})

	it('renders Suite properly', async () => {
		const wrapper = mount(AccreditedTypeChip, {
			global: { plugins: [vuetify] },
			props: { wikibase: { ...testWiki, wikibaseType: WikibaseType.Suite } }
		})

		const tooltip = document.querySelector('.type-tooltip-suite')
		expect(tooltip).not.toBeNull()
		expect(tooltip?.textContent).toEqual('Manually set')

		const chip = wrapper.find('span.wikibase-type-chip')
		expect(chip.exists()).toEqual(true)
		expect(chip.text()).toEqual('Self-Hosted')
	})

	it('renders Test properly', async () => {
		const wrapper = mount(AccreditedTypeChip, {
			global: { plugins: [vuetify] },
			props: { wikibase: { ...testWiki, wikibaseType: WikibaseType.Test } }
		})

		const tooltip = document.querySelector('.type-tooltip-test')
		expect(tooltip).not.toBeNull()
		expect(tooltip?.textContent).toEqual('Manually set')

		const chip = wrapper.find('span.wikibase-type-chip')
		expect(chip.exists()).toEqual(true)
		expect(chip.text()).toEqual('Test')
	})

	it('renders Unknown properly', async () => {
		const wrapper = mount(AccreditedTypeChip, {
			global: { plugins: [vuetify] },
			props: { wikibase: { ...testWiki, wikibaseType: WikibaseType.Unknown } }
		})

		const tooltip = document.querySelector('.type-tooltip-unknown')
		expect(tooltip).not.toBeNull()
		expect(tooltip?.textContent).toEqual('Not set')

		const chip = wrapper.find('span.wikibase-type-chip')
		expect(chip.exists()).toEqual(true)
		expect(chip.text()).toEqual('Unknown')
	})
})
