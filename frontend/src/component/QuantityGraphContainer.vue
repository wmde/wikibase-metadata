<script setup lang="ts">
import LineGraph from '@/component/graph/LineGraph.vue'
import { useWikiQuantityStore } from '@/stores/wikibase-quantity-store.ts'
import stringDate from '@/util/string-date'
import { computed, onBeforeMount } from 'vue'

const store = useWikiQuantityStore()
const data = computed(() => store.wikibases.data)

onBeforeMount(() => store.fetchWikibases())
</script>

<template>
	<v-container class="quantity-graph-container my-0 px-6 py-8">
		<line-graph
			v-if="data?.length"
			:datasets="			data.map((w) => ({
				label: w.title,
				tension: 0.3,
				data: w.quantityObservations.allObservations
					.map((o) =>
						o.totalTriples != null
							? { x: stringDate(o.observationDate).valueOf(), y: o.totalTriples }
							: null
					)
					.filter((p) => p != null)
			}))
"
		/>
	</v-container>
</template>

<style lang="scss"></style>
