import WikibaseCategoryChip from '@/component/wikibase-table/WikibaseCategoryChip.vue'
import type { WikibaseCategory } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

describe('WikibaseCategoryChip', async () => {
	it.each([
		{ arg: 'CULTURAL_AND_HISTORICAL' as WikibaseCategory, expectedTitle: 'Cultural & Historical' },
		{
			arg: 'DIGITAL_COLLECTIONS_AND_ARCHIVES' as WikibaseCategory,
			expectedTitle: 'Digital Collections & Archives'
		},
		{
			arg: 'EDUCATIONAL_AND_REFERENCE_COLLECTIONS' as WikibaseCategory,
			expectedTitle: 'Educational & Reference Collections'
		},
		{
			arg: 'EXPERIMENTAL_AND_PROTOTYPE_PROJECTS' as WikibaseCategory,
			expectedTitle: 'Experimental & Prototype Projects'
		},
		{
			arg: 'FICTIONAL_AND_CREATIVE_WORKS' as WikibaseCategory,
			expectedTitle: 'Fictional & Creative Works'
		},
		{ arg: 'LEGAL_AND_POLITICAL' as WikibaseCategory, expectedTitle: 'Legal & Political' },
		{ arg: 'LINGUISTIC_AND_LITERARY' as WikibaseCategory, expectedTitle: 'Linguistic & Literary' },
		{ arg: 'MATHEMATICS_AND_SCIENCE' as WikibaseCategory, expectedTitle: 'Mathematics & Science' },
		{
			arg: 'SEMANTIC_AND_PROSOPOGRAPHIC_DATA' as WikibaseCategory,
			expectedTitle: 'Semantic & Prosopographic Data'
		},
		{ arg: 'SOCIAL_AND_ADVOCACY' as WikibaseCategory, expectedTitle: 'Social & Advocacy' },
		{
			arg: 'TECHNOLOGY_AND_OPEN_SOURCE' as WikibaseCategory,
			expectedTitle: 'Technology & Open Source'
		},
		{ arg: null, expectedTitle: '–' },
		{ arg: undefined, expectedTitle: '–' }
	])(`renders $arg properly`, async ({ arg, expectedTitle }) => {
		const wrapper = mount(WikibaseCategoryChip, {
			global: { plugins: [vuetify] },
			props: { category: arg }
		})

		const chip = wrapper.find('span.wikibase-category-chip')
		expect(chip.exists()).toEqual(true)
		expect(chip.text()).toEqual(expectedTitle)
	})
})
