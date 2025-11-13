import { WikibaseCategory } from '@/graphql/types'
import vuetify from '@/plugin/vuetify'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import WikibaseCategoryChip from '../WikibaseCategoryChip.vue'

describe('WikibaseCategoryChip', async () => {
	it.each([
		{ arg: WikibaseCategory.CulturalAndHistorical, expectedTitle: 'Cultural & Historical' },
		{
			arg: WikibaseCategory.DigitalCollectionsAndArchives,
			expectedTitle: 'Digital Collections & Archives'
		},
		{
			arg: WikibaseCategory.EducationalAndReferenceCollections,
			expectedTitle: 'Educational & Reference Collections'
		},
		{
			arg: WikibaseCategory.ExperimentalAndPrototypeProjects,
			expectedTitle: 'Experimental & Prototype Projects'
		},
		{
			arg: WikibaseCategory.FictionalAndCreativeWorks,
			expectedTitle: 'Fictional & Creative Works'
		},
		{ arg: WikibaseCategory.LegalAndPolitical, expectedTitle: 'Legal & Political' },
		{ arg: WikibaseCategory.LinguisticAndLiterary, expectedTitle: 'Linguistic & Literary' },
		{ arg: WikibaseCategory.MathematicsAndScience, expectedTitle: 'Mathematics & Science' },
		{
			arg: WikibaseCategory.SemanticAndProsopographicData,
			expectedTitle: 'Semantic & Prosopographic Data'
		},
		{ arg: WikibaseCategory.SocialAndAdvocacy, expectedTitle: 'Social & Advocacy' },
		{ arg: WikibaseCategory.TechnologyAndOpenSource, expectedTitle: 'Technology & Open Source' },
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
