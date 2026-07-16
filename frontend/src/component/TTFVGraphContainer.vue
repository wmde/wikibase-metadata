<script setup lang="ts">
import QGraph from '@/component/graph/QGraph.vue'
import { useWikiTTFVStore } from '@/stores/wikibase-ttfv-store'
import stringDate from '@/util/string-date'
import { computed, onBeforeMount } from 'vue'

const store = useWikiTTFVStore()
const wikibase = computed(() => store.wikibases.data?.[0])

onBeforeMount(() => store.fetchWikibases())
</script>

<template>
	<v-container class="ttfv-graph-container my-0 px-6 py-8">
		<v-container>{{ wikibase }}</v-container>
			<q-graph
				v-if="wikibase?.timeToFirstValueObservations.mostRecent?.initiationDate"
				:dataset="{
					label: 'Q',
					data: [
						{
							x: stringDate(
								wikibase.timeToFirstValueObservations.mostRecent.initiationDate
							).valueOf(),
							y: 0.5
						},
						...wikibase.timeToFirstValueObservations.mostRecent.itemDates.map((v) => ({
							x: stringDate(v.creationDate).valueOf(),
							y: v.q
						}))
					]
				}"
			/>
	</v-container>
</template>

<style lang="scss"></style>
