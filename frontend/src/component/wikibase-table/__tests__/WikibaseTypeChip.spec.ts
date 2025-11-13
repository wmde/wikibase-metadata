import WikibaseTypeChip from '@/component/wikibase-table/WikibaseTypeChip.vue'
import { WikibaseType } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseTypeChip', async () => {
	it.each([
		{ arg: WikibaseType.Cloud, expectedTitle: 'Wikibase Cloud' },
		{ arg: WikibaseType.Other, expectedTitle: 'Other' },
		{ arg: WikibaseType.Suite, expectedTitle: 'Self-Hosted' },
		{ arg: WikibaseType.Test, expectedTitle: 'Test' },
		{ arg: WikibaseType.Unknown, expectedTitle: 'Unknown' }
	])(`renders $arg properly`, async ({ arg, expectedTitle }) => {
		const wrapper = mount(WikibaseTypeChip, {
			global: { plugins: [vuetify] },
			props: { wikibaseType: arg }
		})

		const chip = wrapper.find('span.wikibase-type-chip')
		expect(chip.exists()).toEqual(true)
		expect(chip.text()).toEqual(expectedTitle)
	})
})
