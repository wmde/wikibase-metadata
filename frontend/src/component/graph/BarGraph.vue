<script setup lang="ts">
import {
	BarElement,
	CategoryScale,
	Chart as ChartJS,
	Legend,
	LinearScale,
	Title,
	Tooltip,
	type ChartData
} from 'chart.js'
import { Bar as BarChart } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export type BarChartCategoryDatum = { label: string; value: number | [number, number] | null }

const { data, label } = defineProps<{ data: BarChartCategoryDatum[]; label?: string }>()

const chartData: ChartData<'bar', (number | [number, number] | null)[], unknown> = {
	labels: data.map((v) => v.label),
	datasets: [
		{
			label: label,
			backgroundColor: '#f87979',
			data: data.map((v) => v.value)
		}
	]
}
</script>

<template>
	<BarChart :data="chartData" />
</template>
