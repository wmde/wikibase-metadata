<script setup lang="ts">
import type { WikibaseType } from '@/graphql/types'

defineProps<{ wikibaseType: WikibaseType | null | undefined }>()
</script>

<template>
	<v-chip class="wikibase-type-chip">{{ wikibaseType ?? 'UNKNOWN' }}</v-chip>
</template>

<style lang="css">
.wikibase-type-chip {
	min-width: 40px;
}
</style>
