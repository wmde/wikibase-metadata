<script setup lang="ts">
import WikibaseCardStatBlock from '@/component/wikibase-card/WikibaseCardStatBlock.vue'
import WikibaseIcon from '@/component/wikibase-card/WikibaseIcon.vue'
import type { WbFragment } from '@/graphql/types'
import computeTotalEdits from '@/util/computeTotalEdits'

defineProps<{ wikibase: WbFragment }>()
</script>

<template>
	<v-card variant="outlined" class="wikibase-card ma-1 pa-1">
		<v-container class="card-header ma-0 pa-0">
			<v-container class="ma-0 pa-0">
				<v-container class="url-container ma-0 pa-0">
					<WikibaseIcon :base-url="wikibase.urls.baseUrl" />
					<v-container class="wikibase-url ma-0 pa-0">
						{{ wikibase.title }}
						|
						{{ wikibase.urls.baseUrl }}
					</v-container>
				</v-container>
				<div v-if="wikibase.description" class="description">{{ wikibase.description }}</div>
			</v-container>
			<v-container class="wikibase-type ma-0 pa-0">{{ wikibase.wikibaseType }}</v-container>
		</v-container>
		<v-container class="stat-block-container ma-0 pa-0">
			<WikibaseCardStatBlock
				label="EDITS (30 DAYS)"
				:stat="computeTotalEdits(wikibase.recentChangesObservations)"
			/>
			<WikibaseCardStatBlock
				label="TRIPLES"
				:stat="wikibase.quantityObservations.mostRecent?.totalTriples"
			/>
		</v-container>
	</v-card>
</template>

<style lang="css">
.wikibase-card {
	display: flex;
	flex-flow: column nowrap;
	justify-content: space-between;
	max-width: 500px;
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
	font-weight: 500;
}
.stat-block-container {
	display: flex;
	flex-flow: row nowrap;
}
</style>
