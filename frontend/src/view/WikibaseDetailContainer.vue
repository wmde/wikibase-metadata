<script setup lang="ts">
import LineGraph from '@/component/LineGraph.vue'
import WikibaseDetailCard from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCard.vue'
import { router } from '@/router'
import { useSingleWikiStore } from '@/stores/wikibase-store'
import compareByValue from '@/util/compare-by-value'
import stringDate from '@/util/string-date'
import { computed, onBeforeMount } from 'vue'

const store = useSingleWikiStore()

const loading = computed(() => store.wikibase.loading)
const wikibaseId = computed(() =>
	router.currentRoute.value.params['id']
		? Number.parseInt(router.currentRoute.value.params['id'] as string)
		: undefined
)
const wikibase = computed(() => store.wikibase.data?.wikibase)

const quantObs = computed(() =>
	store.wikibase.data?.wikibase.quantityObservations.allObservations.filter((q) => q.returnedData)
)

onBeforeMount(() => wikibaseId.value && store.searchWikibase(wikibaseId.value))
</script>

<template>
	<v-container class="ma-0 pa-0">
		<WikibaseDetailCard :loading="loading" :wikibase="wikibase" />
		<template v-if="wikibase && !loading">
			<LineGraph
				:datasets="[
					{
						label: 'Triples',
						data:
							quantObs
								?.map((q) => ({
									x: stringDate(q.observationDate).valueOf(),
									y: q.totalTriples ?? null
								}))
								.sort((a, b) => compareByValue(a, b, (v) => v.x)) ?? []
					},
					{
						label: 'Items',
						data:
							quantObs
								?.map((q) => ({
									x: stringDate(q.observationDate).valueOf(),
									y: q.totalItems ?? null
								}))
								.sort((a, b) => compareByValue(a, b, (v) => v.x)) ?? []
					},
					{
						label: 'Properties',
						data:
							quantObs
								?.map((q) => ({
									x: stringDate(q.observationDate).valueOf(),
									y: q.totalProperties ?? null
								}))
								.sort((a, b) => compareByValue(a, b, (v) => v.x)) ?? []
					}
				]"
			/>
		</template>
	</v-container>
</template>
