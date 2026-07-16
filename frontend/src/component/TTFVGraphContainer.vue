<script setup lang="ts">
import MultiQGraph from '@/component/graph/MultiQGraph.vue'
import { useWikiTTFVStore } from '@/stores/wikibase-ttfv-store'
import randomColor from '@/util/random-color'
import stringDate from '@/util/string-date'
import { computed, onBeforeMount } from 'vue'

const store = useWikiTTFVStore()
const data = computed(() => store.wikibases.data)
const randomColorList = computed(() =>
	(store.wikibases.data ?? []).reduce(
		(prev, wiki): Record<string, string> => ({ ...prev, [wiki.id]: randomColor() }),
		{}
	)
)

onBeforeMount(() => store.fetchWikibases())
</script>

<template>
	<v-container class="ttfv-graph-container my-0 px-6 py-8">
		<multi-q-graph
			v-if="data"
			:datasets="
				data.map((wikibase) => ({
					label: wikibase.title,
					tension: 0.3,
					backgroundColor: randomColorList[wikibase.id],
					borderColor: randomColorList[wikibase.id],
					data: [
						wikibase.timeToFirstValueObservations.mostRecent?.initiationDate
							? {
									x: stringDate(
										wikibase.timeToFirstValueObservations.mostRecent.initiationDate
									).valueOf(),
									y: 0.5
								}
							: null,
						...(wikibase.timeToFirstValueObservations.mostRecent?.itemDates ?? []).map((v) => ({
							x: stringDate(v.creationDate).valueOf(),
							y: v.q
						}))
					]
				}))
			"
		/>
	</v-container>
</template>

<style lang="scss"></style>
