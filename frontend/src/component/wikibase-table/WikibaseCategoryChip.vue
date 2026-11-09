<script setup lang="ts">
import type { WikibaseCategory } from '@/graphql/types'
import { mdiTagOutline } from '@mdi/js'

defineProps<{ category: WikibaseCategory | null | undefined; icon?: boolean }>()

const categoryTitle = (cat: WikibaseCategory | null | undefined): string => {
	switch (cat) {
		case 'CULTURAL_AND_HISTORICAL':
			return 'Cultural & Historical'
		case 'DIGITAL_COLLECTIONS_AND_ARCHIVES':
			return 'Digital Collections & Archives'
		case 'EDUCATIONAL_AND_REFERENCE_COLLECTIONS':
			return 'Educational & Reference Collections'
		case 'EXPERIMENTAL_AND_PROTOTYPE_PROJECTS':
			return 'Experimental & Prototype Projects'
		case 'FICTIONAL_AND_CREATIVE_WORKS':
			return 'Fictional & Creative Works'
		case 'LEGAL_AND_POLITICAL':
			return 'Legal & Political'
		case 'LINGUISTIC_AND_LITERARY':
			return 'Linguistic & Literary'
		case 'MATHEMATICS_AND_SCIENCE':
			return 'Mathematics & Science'
		case 'SEMANTIC_AND_PROSOPOGRAPHIC_DATA':
			return 'Semantic & Prosopographic Data'
		case 'SOCIAL_AND_ADVOCACY':
			return 'Social & Advocacy'
		case 'TECHNOLOGY_AND_OPEN_SOURCE':
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
