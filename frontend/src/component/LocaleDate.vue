<script setup lang="ts">
import stringDate from '@/util/stringDate'

defineProps<{ stat: Date | string | null | undefined }>()
</script>

<template>
	<template v-if="stat != null && stat != undefined">
		{{ stringDate(stat).toLocaleDateString('de') }}
	</template>
	<template v-else>–</template>
</template>

<style lang="css"></style>
