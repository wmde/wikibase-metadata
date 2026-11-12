import WikibaseTypeChip from '@/component/wikibase-table/WikibaseTypeChip.vue'
import type { WikibaseType } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseTypeChip', async () => {
	it.each([
		{ arg: 'CLOUD' as WikibaseType, expectedTitle: 'Wikibase Cloud' },
		{ arg: 'OTHER' as WikibaseType, expectedTitle: 'Other' },
		{ arg: 'SUITE' as WikibaseType, expectedTitle: 'Self-Hosted' },
		{ arg: 'TEST' as WikibaseType, expectedTitle: 'Test' },
		{ arg: 'UNKNOWN' as WikibaseType, expectedTitle: 'Unknown' }
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
