<script setup lang="ts">
import { computed } from 'vue'

const { value } = defineProps<{ label: string; value: number | Date }>()
const valueString = computed(() =>
	value instanceof Date ? value.toLocaleString('de').replace(',', '') : value.toLocaleString('en')
)
</script>

<template>
	<v-container class="ma-0 p-4 statistic">
		<v-container class="ma-0 pa-0 statistic-label shrink">
			{{ label }}
		</v-container>
		<v-container class="ma-0 pa-0 statistic-value shrink">
			{{ valueString }}
		</v-container>
	</v-container>
</template>

<style lang="css">
.statistic {
	display: flex;
	flex-flow: row nowrap;
	justify-content: space-between;
	align-items: baseline;
	background-color: oklch(98.5% 0.002 247.839);
	border: 1px solid oklch(92.8% 0.006 264.531);
	border-radius: 0.25rem;
}
.statistic-label {
	font-family: Roboto;
	font-size: 16px;
	color: rgb(0, 0, 0);
}
.statistic-value {
	font-family: Roboto;
	font-size: 16px;
	color: rgb(0, 0, 0);
	font-weight: 500;
}
</style>
