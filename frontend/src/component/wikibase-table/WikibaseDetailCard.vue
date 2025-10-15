<script setup lang="ts">
import WikibaseCardStatBlock from '@/component/wikibase-card/WikibaseCardStatBlock.vue'
import WikibaseIcon from '@/component/wikibase-card/WikibaseIcon.vue'
import { useSingleWikiStore } from '@/stores/wikibase-store'
import computeTotalEdits from '@/util/computeTotalEdits'
import stringDate from '@/util/stringDate'
import { computed, onBeforeMount } from 'vue'

const props = defineProps<{ wikibaseId: number }>()

const store = useSingleWikiStore()
const wikibase = computed(() => store.wikibase.data?.wikibase)
const loading = computed(() => store.wikibase.loading)

onBeforeMount(() => store.searchWikibase(props.wikibaseId))
</script>

<template>
	<v-skeleton-loader
		class="wikibase-detail-card-loader"
		v-if="loading"
		color="secondary"
		type="card"
	>
		LOADING
	</v-skeleton-loader>
	<v-card v-if="wikibase" variant="outlined" class="wikibase-detail-card ma-1 pa-1">
		<v-container class="card-header ma-0 pa-0">
			<v-container class="ma-0 pa-0">
				<v-container class="url-container ma-0 pa-0">
					<WikibaseIcon :base-url="wikibase.urls.baseUrl" />
					<v-container class="wikibase-url ma-0 pa-0">
						<a :href="wikibase.urls.baseUrl">
							{{ wikibase.title }}
						</a>
					</v-container>
					<v-container v-if="wikibase.urls.sparqlFrontendUrl" class="wikibase-url ma-0 pa-0">
						<a :href="wikibase.urls.sparqlFrontendUrl"> SPARQL </a>
					</v-container>
				</v-container>
				<div v-if="wikibase.description" class="description">{{ wikibase.description }}</div>
			</v-container>
			<v-container class="wikibase-type ma-0 pa-0">{{ wikibase.wikibaseType }}</v-container>
		</v-container>
		<v-container
			v-if="wikibase.timeToFirstValueObservations.mostRecent?.initiationDate"
			class="stat-block-container ma-0 pa-0"
		>
			<v-label>
				FIRST RECORD
				{{
					stringDate(
						wikibase.timeToFirstValueObservations.mostRecent?.initiationDate
					).toLocaleDateString()
				}}
			</v-label>
			<v-label>
				AS OF
				{{
					stringDate(
						wikibase.timeToFirstValueObservations.mostRecent?.observationDate
					).toLocaleDateString()
				}}
			</v-label>
		</v-container>
		<v-container
			v-if="wikibase.quantityObservations.mostRecent"
			class="stat-block-container ma-0 pa-0"
		>
			<WikibaseCardStatBlock
				label="ITEMS"
				:stat="wikibase.quantityObservations.mostRecent?.totalItems"
			/>
			<WikibaseCardStatBlock
				label="PROPERTIES"
				:stat="wikibase.quantityObservations.mostRecent?.totalProperties"
			/>
			<WikibaseCardStatBlock
				label="LEXEMES"
				:stat="wikibase.quantityObservations.mostRecent?.totalLexemes"
			/>
			<WikibaseCardStatBlock
				label="TRIPLES"
				:stat="wikibase.quantityObservations.mostRecent?.totalTriples"
			/>
			<v-label>
				AS OF
				{{
					stringDate(wikibase.quantityObservations.mostRecent?.observationDate).toLocaleDateString()
				}}
			</v-label>
		</v-container>
		<v-container
			v-if="wikibase.recentChangesObservations.mostRecent"
			class="stat-block-container ma-0 pa-0"
		>
			<WikibaseCardStatBlock
				label="EDITS (30 DAYS)"
				:stat="computeTotalEdits(wikibase.recentChangesObservations)"
			/>
			<v-label>
				AS OF
				{{
					stringDate(
						wikibase.recentChangesObservations.mostRecent?.observationDate
					).toLocaleDateString()
				}}
			</v-label>
		</v-container>
	</v-card>
</template>

<style lang="css">
.wikibase-detail-card-loader {
	background-color: white;
}
.wikibase-detail-card {
	display: flex;
	flex-flow: column nowrap;
	justify-content: space-between;
	max-width: 500px;
	background-color: white;
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
	flex-flow: row wrap;
}
.stat-block-container .stat-container,
.stat-block-container .v-label {
	width: auto;
	margin: 4px;
}
</style>
