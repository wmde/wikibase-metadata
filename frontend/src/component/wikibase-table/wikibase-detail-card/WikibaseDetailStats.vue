<script setup lang="ts">
import WikibaseStatistic from '@/component/wikibase-table/wikibase-detail-card/WikibaseStatistic.vue';
import type { SingleWikibaseFragment } from '@/graphql/types';
import stringDate from '@/util/string-date';

defineProps<{ wikibase: SingleWikibaseFragment }>()
</script>

<template>
	<v-container class="ma-0 pa-0 pb-8 statistics-container">
		<v-container class="ma-0 mb-4 pa-0 title">Statistics</v-container>
		<v-container class="ma-0 pa-0 stats-container">
			<WikibaseStatistic
				v-if="wikibase.quantityObservations.mostRecent?.totalTriples != null"
				label="Total Triples"
				:value="wikibase.quantityObservations.mostRecent.totalTriples"
			/>
			<WikibaseStatistic
				v-if="wikibase.recentChangesObservations.mostRecent"
				label="Edits (Last 30 days)"
				:value="
					(wikibase.recentChangesObservations.mostRecent?.botChangeCount ?? 0) +
					(wikibase.recentChangesObservations.mostRecent?.humanChangeCount ?? 0)
				"
			/>
			<WikibaseStatistic
				v-if="wikibase.quantityObservations.mostRecent?.totalItems != null"
				label="Items"
				:value="wikibase.quantityObservations.mostRecent.totalItems"
			/>
			<WikibaseStatistic
				v-if="wikibase.quantityObservations.mostRecent?.totalProperties != null"
				label="Properties"
				:value="wikibase.quantityObservations.mostRecent.totalProperties"
			/>
			<WikibaseStatistic
				v-if="wikibase.quantityObservations.mostRecent?.totalLexemes != null"
				label="Lexemes"
				:value="wikibase.quantityObservations.mostRecent.totalLexemes"
			/>
			<WikibaseStatistic
				v-if="wikibase.timeToFirstValueObservations.mostRecent?.initiationDate != null"
				label="First Record"
				:value="stringDate(wikibase.timeToFirstValueObservations.mostRecent?.initiationDate)"
			/>
		</v-container>
	</v-container>
</template>

<style lang="css">
.stats-container {
	display: flex;
	flex-flow: column nowrap;
	gap: 0.75rem;
}
.statistics-container .title {
	font-family: Montserrat;
	font-weight: 700;
	font-size: 20px;
	color: rgb(0, 0, 0);
}
</style>
