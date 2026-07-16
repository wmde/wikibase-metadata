<script setup lang="ts">
import LineGraph from '@/component/graph/LineGraph.vue'
import { useWikiQuantityStore } from '@/stores/wikibase-quantity-store.ts'
import stringDate from '@/util/string-date'
import type { Point } from 'chart.js'
import { computed, onBeforeMount } from 'vue'

const store = useWikiQuantityStore()
const data = computed(() => store.wikibases.data)


const sortByX = (a: Point, b: Point) =>
	a.x == null && b.x == null
		? 0
		: a.x == null
			? -1
			: b.x == null
				? 1
				: a.x > b.x
					? 1
					: a.x < b.x
						? -1
						: 0

onBeforeMount(() => store.fetchWikibases())
</script>

<template>
	<v-container class="quantity-graph-container my-0 px-6 py-8">
		<line-graph
			v-if="data?.length"
			title="Items"
			:datasets="
				data.map((w) => ({
					label: w.title,
					tension: 0.3,
					data: w.quantityObservations.allObservations
						.map((o) =>
							o.totalItems != null
								? { x: stringDate(o.observationDate).valueOf(), y: o.totalItems }
								: null
						)
						.filter((p) => p != null)
						.sort(sortByX)
				}))
			"
		/>
		<line-graph
			v-if="data?.length"
			title="Lexemes"
			:datasets="
				data.map((w) => ({
					label: w.title,
					tension: 0.3,
					data: w.quantityObservations.allObservations
						.map((o) =>
							o.totalLexemes != null
								? { x: stringDate(o.observationDate).valueOf(), y: o.totalLexemes }
								: null
						)
						.filter((p) => p != null)
						.sort(sortByX)
				}))
			"
		/>
		<line-graph
			v-if="data?.length"
			title="Properties"
			:datasets="
				data.map((w) => ({
					label: w.title,
					tension: 0.3,
					data: w.quantityObservations.allObservations
						.map((o) =>
							o.totalProperties != null
								? { x: stringDate(o.observationDate).valueOf(), y: o.totalProperties }
								: null
						)
						.filter((p) => p != null)
						.sort(sortByX)
				}))
			"
		/>
		<line-graph
			v-if="data?.length"
			title="Triples"
			:datasets="
				data.map((w) => ({
					label: w.title,
					tension: 0.3,
					data: w.quantityObservations.allObservations
						.map((o) =>
							o.totalTriples != null
								? { x: stringDate(o.observationDate).valueOf(), y: o.totalTriples }
								: null
						)
						.filter((p) => p != null)
						.sort(sortByX)
				}))
			"
		/>
	</v-container>
</template>

<style lang="scss"></style>
