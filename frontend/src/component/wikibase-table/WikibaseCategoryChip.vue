<script setup lang="ts">
import { WikibaseCategory } from '@/graphql/types'

defineProps<{ category: WikibaseCategory | null | undefined }>()

const categoryTitle = (cat: WikibaseCategory | null | undefined): string => {
	switch (cat) {
		case WikibaseCategory.CulturalAndHistorical:
			return 'Cultural & Historical'
		case WikibaseCategory.DigitalCollectionsAndArchives:
			return 'Digital Collections & Archives'
		case WikibaseCategory.EducationalAndReferenceCollections:
			return 'Educational & Reference Collections'
		case WikibaseCategory.ExperimentalAndPrototypeProjects:
			return 'Experimental & Prototype Projects'
		case WikibaseCategory.FictionalAndCreativeWorks:
			return 'Fictional & Creative Works'
		case WikibaseCategory.LegalAndPolitical:
			return 'Legal & Political'
		case WikibaseCategory.LinguisticAndLiterary:
			return 'Linguistic & Literary'
		case WikibaseCategory.MathematicsAndScience:
			return 'Mathematics & Science'
		case WikibaseCategory.SemanticAndProsopographicData:
			return 'Semantic & Prosopographic Data'
		case WikibaseCategory.SocialAndAdvocacy:
			return 'Social & Advocacy'
		case WikibaseCategory.TechnologyAndOpenSource:
			return 'Technology & Open Source'
		default:
			return '–'
	}
}
</script>

<template>
	<v-chip class="wikibase-category-chip">{{ categoryTitle(category) }}</v-chip>
</template>
