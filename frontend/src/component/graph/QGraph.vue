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

const { dataset } = defineProps<{ dataset: ChartDataset<'line', (number | Point | null)[]> }>()

const chartData: ChartData<'line', (number | Point | null)[], unknown> = {
	datasets: [
		{
			...dataset,
			backgroundColor: '#ff49e7',
			borderColor: '#ff49e7',
			yAxisID: 'y'
		}
	]
}
</script>

<template>
	<LineChart
		:data="chartData"
		:options="{
			plugins: {
				tooltip: {
					callbacks: {
						title: (items) =>
							items[0]?.parsed.y == 0.5
								? `First Record: ${new Date(items[0]?.parsed.x ?? 0).toLocaleDateString('de')}`
								: `Q${items[0]?.parsed.y?.toLocaleString('de')}: ${new Date(items[0]?.parsed.x ?? 0).toLocaleDateString('de')}`,
						label: () => ''
					}
				}
			},
			responsive: true,
			scales: {
				x: {
					type: 'linear',
					ticks: { callback: (tickValue) => new Date(tickValue).toLocaleDateString('de') }
				},
				y: {
					grid: { drawOnChartArea: true },
					min: 0.5,
					ticks: {
						callback: (tickValue) =>
							typeof tickValue == 'number' && Math.log10(tickValue) % 1 == 0
								? `Q${tickValue.toLocaleString('de')}`
								: ''
					},
					type: 'logarithmic'
				}
			}
		}"
	/>
</template>
