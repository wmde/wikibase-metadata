<script setup lang="ts">
import { WikibaseType } from '@/graphql/types'

defineProps<{ wikibaseType: WikibaseType | null | undefined }>()

const typeTitle = (t: WikibaseType | null | undefined): string => {
	switch (t) {
		case WikibaseType.Cloud:
			return 'Wikibase Cloud'
		case WikibaseType.Other:
			return 'Other'
		case WikibaseType.Suite:
			return 'Self-Hosted'
		case WikibaseType.Test:
			return 'Test'
		default:
			return 'Unknown'
	}
}
</script>

<template>
	<v-chip class="wikibase-type-chip">{{ typeTitle(wikibaseType) }}</v-chip>
</template>
