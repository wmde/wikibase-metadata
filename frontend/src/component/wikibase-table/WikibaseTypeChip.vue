<script setup lang="ts">
import { WikibaseType } from '@/graphql/types'
import typeTitle from '@/util/type-title'

defineProps<{ wikibaseType: WikibaseType | null | undefined }>()
</script>

<template>
	<v-chip class="wikibase-type-chip">{{ typeTitle(wikibaseType) }}</v-chip>
</template>
