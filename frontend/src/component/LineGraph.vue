<script setup lang="ts">
import {
	CategoryScale,
	Chart as ChartJS,
	Legend,
	LinearScale,
	LineElement,
	PointElement,
	Title,
	Tooltip,
	type ChartData,
	type ChartDataset,
	type Point
} from 'chart.js'
import { Line as LineChart } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const { datasets } = defineProps<{ datasets: ChartDataset<'line', (number | Point | null)[]>[] }>()

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

const chartData: ChartData<'line', (number | Point | null)[], unknown> = {
	datasets: datasets.map((d, idx) => ({
		...d,
		backgroundColor: colors[idx % colors.length],
		borderColor: colors[idx % colors.length],
		yAxisID: `y${idx}`
	}))
}
</script>

<template>
	<LineChart
		:data="chartData"
		:options="{
			responsive: true,
			scales: {
				x: {
					type: 'linear',
					ticks: { callback: (tickValue) => new Date(tickValue).toLocaleDateString('de') },
					max: new Date().getTime()
				},
				...Object.fromEntries(
					datasets.map((d, idx) => [
						`y${idx}`,
						{
							grid: { drawOnChartArea: idx == 0 },
							title: { display: true, text: d.label }
						}
					])
				)
			}
		}"
	/>
</template>
