<script setup lang="ts">
import {
	Chart as ChartJS,
	Legend,
	LinearScale,
	LineElement,
	LogarithmicScale,
	PointElement,
	Title,
	Tooltip,
	type ChartData,
	type ChartDataset,
	type Point
} from 'chart.js'
import { Line as LineChart } from 'vue-chartjs'

ChartJS.register(LinearScale, LogarithmicScale, PointElement, LineElement, Title, Tooltip, Legend)

const { datasets } = defineProps<{
	datasets: ChartDataset<'line', Point[]>[]
	title: string
}>()

const colors = [
	'#73f8a0',
	'#efc4b3',
	'#ff49e7',
	'#b89402',
	'#df50c8',
	'#1f7979',
	'#05cb9e',
	'#131cc8',
	'#81c86f',
	'#f258fe'
]

const chartData: ChartData<'line', Point[], unknown> = {
	datasets: datasets
		.filter((d) => d.data.some((v) => v.y != null && v.y > 0))
		.map((d, idx) => ({
			...d,
			backgroundColor: colors[idx % colors.length],
			borderColor: colors[idx % colors.length],
			// yAxisID: `y${idx}`
			yAxisID: 'y'
		}))
}
</script>

<template>
	<v-container>{{ title }}</v-container>
	<LineChart
		:data="chartData"
		:options="{
			plugins: {
				tooltip: {
					callbacks: {
						title: (items) => new Date(items[0]?.parsed.x ?? 0).toLocaleDateString('de')
					}
				}
			},
			responsive: true,
			scales: {
				x: {
					type: 'linear',
					ticks: { callback: (tickValue) => new Date(tickValue).toLocaleDateString('de') },
					max: new Date().getTime()
				},
				y: {
					type: 'logarithmic'
				}
				// ...Object.fromEntries(
				// 	datasets.map((d, idx) => [
				// 		`y${idx}`,
				// 		{
				// 			grid: { drawOnChartArea: idx == 0 },
				// 			title: { display: true, text: d.label }
				// 		}
				// 	])
				// )
			}
		}"
	/>
</template>
