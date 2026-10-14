<script setup lang="ts">
import WikibaseHistoryDetail from '@/component/wikibase-table/wikibase-detail-card/WikibaseHistoryDetail.vue'
import type { WikibaseTimeToFirstValueObservation } from '@/graphql/types'

defineProps<{ obs: Partial<WikibaseTimeToFirstValueObservation> }>()
</script>

<template>
	<v-expansion-panels class="history-container" flat v-if="obs.initiationDate || obs.itemDates">
		<v-expansion-panel>
			<v-expansion-panel-title class="title">Edit History</v-expansion-panel-title>
			<v-expansion-panel-text class="ma-0 pa-0">
				<wikibase-history-detail :obs="obs" />
			</v-expansion-panel-text>
		</v-expansion-panel>
	</v-expansion-panels>
</template>

<style lang="scss">
.history-container {
	.v-expansion-panel-text__wrapper {
		padding: 0.75rem 0 0;
	}
	.title {
		font-family: Montserrat;
		font-weight: 700;
		font-size: 20px;
		color: rgb(0, 0, 0);
		background-color: oklch(98.5% 0.002 247.839);
		border: 1px solid oklch(92.8% 0.006 264.531);
		border-radius: 0.25rem;
	}
}
</style>
