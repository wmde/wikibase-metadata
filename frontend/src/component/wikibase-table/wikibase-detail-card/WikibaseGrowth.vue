<script setup lang="ts">
import WikibaseGrowthMilestone from '@/component/wikibase-table/wikibase-detail-card/WikibaseGrowthMilestone.vue'
import type { WikibaseTimeToFirstValueObservation } from '@/graphql/types'
import stringDate from '@/util/string-date'

defineProps<{ obs: Partial<WikibaseTimeToFirstValueObservation> }>()
</script>

<template>
	<v-expansion-panels class="growth-container" flat v-if="obs.initiationDate || obs.itemDates">
		<v-expansion-panel>
			<v-expansion-panel-title class="title">Growth Milestones</v-expansion-panel-title>
			<v-expansion-panel-text class="ma-0 pa-0">
				<v-container class="ma-0 pa-0 grow-container">
					<WikibaseGrowthMilestone
						v-if="obs.initiationDate"
						label="First Record"
						:entities="1"
						:entity-date="stringDate(obs.initiationDate)"
					/>
					<WikibaseGrowthMilestone
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

<style lang="css">
.grow-container {
	display: flex;
	flex-flow: column nowrap;
	gap: 0.75rem;
}
.growth-container .v-expansion-panel-text__wrapper {
	padding: 0.75rem 0 0;
}
.growth-container .title {
	font-family: Montserrat;
	font-weight: 700;
	font-size: 20px;
	color: rgb(0, 0, 0);
	background-color: oklch(98.5% 0.002 247.839);
	border: 1px solid oklch(92.8% 0.006 264.531);
	border-radius: 0.25rem;
}
</style>
