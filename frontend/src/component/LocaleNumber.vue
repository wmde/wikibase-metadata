<script setup lang="ts">
defineProps<{ stat: number | null | undefined }>()
</script>

<template>
	<template v-if="stat != null && stat != undefined">
		{{ stat.toLocaleString('en') }}
	</template>
	<template v-else>–</template>
</template>
