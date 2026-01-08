<script setup lang="ts">
import stringDate from '@/util/string-date'

defineProps<{ stat: Date | string | null | undefined }>()
</script>

<template>
	<template v-if="stat != null && stat != undefined">
		{{ stringDate(stat).toLocaleDateString('de') }}
		{{ stringDate(stat).toLocaleTimeString('de') }}
	</template>
	<template v-else>–</template>
</template>
