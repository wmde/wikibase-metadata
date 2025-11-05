<script setup lang="ts">
defineProps<{ stat: number | null | undefined }>()
</script>

<template>
	<template v-if="stat != null && stat != undefined">
		{{ stat.toLocaleString('de') }}
	</template>
	<template v-else>–</template>
</template>
