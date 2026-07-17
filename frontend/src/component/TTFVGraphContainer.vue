<script setup lang="ts">
import MultiQGraph from '@/component/graph/MultiQGraph.vue'
import type { WikibaseItemDate } from '@/graphql/types'
import { useWikiTTFVStore } from '@/stores/wikibase-ttfv-store'
import computeTimedelta, { isNegative } from '@/util/compute-timedelta'
import randomColor from '@/util/random-color'
import stringDate from '@/util/string-date'
import { computed, onBeforeMount } from 'vue'
import BarGraph from './graph/BarGraph.vue'

const store = useWikiTTFVStore()
const data = computed(() => store.wikibases.data)
const timedeltaData = computed(() =>
	data.value
		?.map((wikibase) => {
			const initiationDate = wikibase.timeToFirstValueObservations.mostRecent?.initiationDate
				? stringDate(wikibase.timeToFirstValueObservations.mostRecent.initiationDate)
				: null
			const firstValueDate =
				wikibase.timeToFirstValueObservations.mostRecent?.itemDates.reduce(
					(prev: Date | null, value: WikibaseItemDate): Date =>
						prev == null
							? stringDate(value.creationDate)
							: prev < stringDate(value.creationDate)
								? prev
								: stringDate(value.creationDate),
					null
				) ?? null
			return { initiationDate, firstValueDate }
		})
		.map((p) =>
			p.firstValueDate == null || p.initiationDate == null
				? null
				: computeTimedelta(p.firstValueDate.valueOf() - p.initiationDate.valueOf())
		)
		.filter((v) => v != null)
)
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
		<bar-graph
			v-if="timedeltaData"
			:data="[
				{ label: 'Negative (Data Error)', value: timedeltaData.filter(isNegative).length },
				{
					label: '<1 Day',
					value: timedeltaData.filter((t) => t.days < 1 && !isNegative(t)).length
				},
				{ label: '1 Day', value: timedeltaData.filter((t) => t.days == 1).length },
				{ label: '2-6 Days', value: timedeltaData.filter((t) => t.days >= 2 && t.days < 7).length },
				{
					label: '7-13 Days',
					value: timedeltaData.filter((t) => t.days >= 7 && t.days < 14).length
				},
				{
					label: '14-27 Days',
					value: timedeltaData.filter((t) => t.days >= 14 && t.days < 28).length
				},
				{ label: '14+ Days', value: timedeltaData.filter((t) => t.days >= 28).length }
			]"
			label="Wiki Count"
		/>
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
