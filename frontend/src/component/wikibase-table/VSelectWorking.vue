<script setup lang="ts">
import { ref, watch } from 'vue'

const { onChange } = defineProps<{ onChange: (value: number) => void }>()

const internalValue = ref(25)
watch(internalValue, () => onChange(internalValue.value))
</script>

<template>
	<v-select
		class="selection ma-0 pa-0"
		:items="[25, 50, 100]"
		v-model="internalValue"
		width="6rem"
		height="1.75rem"
		density="compact"
		variant="outlined"
	/>
</template>

<style lang="css">
.selection {
	font-family: Roboto;
	font-size: 16px;
	border-color: oklch(87.2 0.01 285.338);
	border-radius: calc(0.625rem - 2px);
}
.selection .v-input__details {
	display: none;
}
</style>
