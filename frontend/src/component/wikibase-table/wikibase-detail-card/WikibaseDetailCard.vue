<script setup lang="ts">
import AccreditedTypeChip from '@/component/wikibase-table/wikibase-detail-card/AccreditedTypeChip.vue'
import CardLoader from '@/component/wikibase-table/wikibase-detail-card/CardLoader.vue'
import WikibaseDescription from '@/component/wikibase-table/wikibase-detail-card/WikibaseDescription.vue'
import WikibaseDetailStats from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailStats.vue'
import WikibaseIcon from '@/component/wikibase-table/wikibase-detail-card/WikibaseIcon.vue'
import WikibaseQueryServiceLink from '@/component/wikibase-table/wikibase-detail-card/WikibaseQueryServiceLink.vue'
import WikibaseTitle from '@/component/wikibase-table/wikibase-detail-card/WikibaseTitle.vue'
import WikibaseCategoryChip from '@/component/wikibase-table/WikibaseCategoryChip.vue'
import type { SingleWikibaseFragment } from '@/graphql/types'
import { useTheme } from 'vuetify'

defineProps<{ wikibase: SingleWikibaseFragment | undefined; loading: boolean }>()

const theme = useTheme()
</script>

<template>
	<v-card
		variant="outlined"
		class="wikibase-detail-card ma-1 pa-1"
		:style="{ backgroundColor: theme.current.value.colors.background }"
	>
		<CardLoader v-if="loading" />
		<template v-else-if="wikibase">
			<v-container class="card-header ma-0 pa-0">
				<v-container class="ma-0 pa-0">
					<v-container class="url-container ma-0 pa-0">
						<WikibaseIcon :base-url="wikibase.urls.baseUrl" />
						<WikibaseTitle :wikibase="wikibase" />
						<WikibaseQueryServiceLink :wikibase="wikibase" />
					</v-container>
					<v-tooltip v-if="wikibase.category" class="desc-tooltip" text="Manually chosen">
						<template v-slot:activator="{ props }">
							<WikibaseCategoryChip :category="wikibase.category" v-bind="props" class="category" />
						</template>
					</v-tooltip>
					<WikibaseDescription :wikibase="wikibase" />
				</v-container>
				<v-container class="wikibase-type ma-0 pa-0">
					<AccreditedTypeChip :wikibase="wikibase" />
				</v-container>
			</v-container>
			<WikibaseDetailStats :wikibase="wikibase" />
		</template>
	</v-card>
</template>

<style lang="css">
.wikibase-detail-card {
	display: flex;
	flex-flow: column nowrap;
	justify-content: space-between;
	max-width: 500px;
	border-color: rgba(255, 255, 255, 0.12);
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
