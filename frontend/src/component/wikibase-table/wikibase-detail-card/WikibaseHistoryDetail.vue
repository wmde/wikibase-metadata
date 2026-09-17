<script setup lang="ts">
import WikibaseMilestone from '@/component/wikibase-table/wikibase-detail-card/WikibaseMilestone.vue'
import type { WikibaseTimeToFirstValueObservation } from '@/graphql/types'
import stringDate from '@/util/string-date'

defineProps<{ obs: Partial<WikibaseTimeToFirstValueObservation> }>()
</script>

<template>
	<v-container class="ma-0 pa-0 milestone-container">
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
</template>

<style lang="scss">
.history-container {
	.milestone-container {
		display: flex;
		flex-flow: column nowrap;
		gap: 0.75rem;
	}
}
</style>
