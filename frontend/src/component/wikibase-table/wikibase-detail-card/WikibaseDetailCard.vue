<script setup lang="ts">
import CardLoader from '@/component/wikibase-table/wikibase-detail-card/CardLoader.vue'
import WikibaseAccess from '@/component/wikibase-table/wikibase-detail-card/WikibaseAccess.vue'
import WikibaseDescription from '@/component/wikibase-table/wikibase-detail-card/WikibaseDescription.vue'
import WikibaseDetailStats from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailStats.vue'
import WikibaseTitle from '@/component/wikibase-table/wikibase-detail-card/WikibaseTitle.vue'
import WikibaseCategoryChip from '@/component/wikibase-table/WikibaseCategoryChip.vue'
import WikibaseTypeChip from '@/component/wikibase-table/WikibaseTypeChip.vue'
import type { SingleWikibaseFragment } from '@/graphql/types'
import { useTheme } from 'vuetify'

defineProps<{ wikibase: SingleWikibaseFragment | undefined; loading: boolean }>()

const theme = useTheme()
</script>

<template>
	<v-card
		variant="outlined"
		class="wikibase-detail-card ma-0 pa-6"
		:style="{ backgroundColor: theme.current.value.colors.background }"
	>
		<CardLoader v-if="loading" />
		<template v-else-if="wikibase">
			<v-container class="ma-0 pa-0 pb-8">
				<WikibaseTitle :wikibase="wikibase" />
				<v-container class="ma-0 pa-0 mb-4 tag-container">
					<WikibaseCategoryChip :category="wikibase.category" class="category" />
					<WikibaseTypeChip :wikibase-type="wikibase.wikibaseType" />
				</v-container>
				<WikibaseDescription :wikibase="wikibase" />
			</v-container>
			<WikibaseDetailStats :wikibase="wikibase" />
			<WikibaseAccess :wikibase="wikibase" />
		</template>
	</v-card>
</template>

<style lang="css">
.wikibase-detail-card {
	max-width: 500px;
	border-color: rgba(255, 255, 255, 0.12);
	border-radius: 0.625rem !important;
}
.tag-container {
	display: flex;
	flex-flow: row wrap;
	gap: 0.75rem;
}
.card-header {
	display: flex;
	flex-flow: row nowrap;
	gap: 12px;
}
.url-container {
	display: flex;
	flex-flow: row wrap;
	justify-content: flex-start;
	gap: 4px;
	align-items: center;
}
.url-container a {
	color: inherit;
}
.wikibase-url {
	width: auto;
}
.wikibase-type {
	width: auto;
	align-self: stretch;
	align-content: center;
}
.wikibase-type-chip {
	min-width: 40px;
	font-weight: 500;
}
.stat-block-container {
	border: 2px solid grey;
	margin: 6px 0;
}
.stats-container {
	display: flex;
	flex-flow: column nowrap;
	margin: 0;
	padding: 0;
}
.stat-source-container {
	color: grey;
	/* margin: 0; */
	/* padding: 4px; */
}
.stat-block-container .stat-container,
.stat-block-container .v-label {
	width: auto;
	margin: 4px;
}
</style>
