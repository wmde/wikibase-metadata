<script setup lang="ts">
import { WikibaseCategory } from '@/graphql/types'
import { mdiTagOutline } from '@mdi/js'

defineProps<{ category: WikibaseCategory | null | undefined; icon?: boolean }>()

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
	<v-chip
		:class="`wikibase-category-chip ${icon ? 'wikibase-category-chip-icon' : ''}`"
		:prepend-icon="icon ? mdiTagOutline : undefined"
		size="large"
		density="compact"
	>
		{{ categoryTitle(category) }}
	</v-chip>
</template>

<style lang="css">
.wikibase-category-chip {
	border-radius: calc(0.625rem - 2px);
	padding-block: 0.125rem;
}
.wikibase-category-chip-icon {
	padding: 4px 8px 4px 16px !important;
}
.wikibase-category-chip .v-chip__content {
	font-family: Roboto;
	font-size: 16px;
	font-weight: 500;
}
.wikibase-category-chip .v-chip__prepend {
	font-size: 10px;
	font-weight: 200;
	margin-right: 0.25rem;
}
</style>
