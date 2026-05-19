<script setup lang="ts">
import WikibaseMilestone from '@/component/wikibase-table/wikibase-detail-card/WikibaseMilestone.vue'
import type { WikibaseTimeToFirstValueObservation } from '@/graphql/types'
import stringDate from '@/util/string-date'

defineProps<{ obs: Partial<WikibaseTimeToFirstValueObservation> }>()
</script>

<template>
	<v-expansion-panels class="history-container" flat v-if="obs.initiationDate || obs.itemDates">
		<v-expansion-panel>
			<v-expansion-panel-title class="title">Edit History</v-expansion-panel-title>
			<v-expansion-panel-text class="ma-0 pa-0">
				<v-container class="ma-0 pa-0 grow-container">
					<WikibaseMilestone
						v-if="obs.initiationDate"
						label="First Record"
						:entities="1"
						:entity-date="stringDate(obs.initiationDate)"
					/>
					<WikibaseMilestone
						v-for="item in obs.itemDates"
						:key="item.id"
						:label="`Q${item.q}`"
						:entities="item.q"
						:entity-date="stringDate(item.creationDate)"
					/>
				</v-container>
			</v-expansion-panel-text>
		</v-expansion-panel>
	</v-expansion-panels>
</template>

<style lang="scss">
.growth-container {
	.grow-container {
		display: flex;
		flex-flow: column nowrap;
		gap: 0.75rem;
	}
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
