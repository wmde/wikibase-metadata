<script setup lang="ts">
import powerOfThousand from '@/util/power-of-thousand'

const { value } = defineProps<{ label: string; value: number }>()
const split = powerOfThousand(value)
const powerString = (power: number) => {
	const dict: Record<number, string> = { 0: '', 1: 'Th', 2: 'M', 3: 'B', 4: 'T' }
	return dict[power]
}
const roundValue = (value: number): number => Math.round(value * 10) / 10
</script>

<template>
	<v-container class="wikibase-total-box ma-0 pa-6">
		<v-container class="value ma-0 pa-0 mb-1">
			<span>
				{{ roundValue(split.value) }}
			</span>
			<span>
				{{ powerString(split.power) }}
			</span>
		</v-container>
		<v-container class="label ma-0 pa-0">{{ label }}</v-container>
	</v-container>
</template>

<style lang="scss">
.wikibase-total-box {
	width: auto;
	flex-grow: 1;
	background-color: #fff;
	border: 1px solid rgba(0, 0, 0, 0.1);
	border-radius: 0.625rem;
	.label {
		font-family: Roboto;
		font-size: 16px;
		color: rgb(0, 0, 0);
	}
	.value {
		font-family: Montserrat;
		color: rgb(0, 0, 0);
		font-weight: 700;
		font-size: 1.875rem;
		line-height: calc(2.25 / 1.875);
	}
}
</style>
