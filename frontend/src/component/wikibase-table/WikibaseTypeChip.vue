<script setup lang="ts">
import { WikibaseType } from '@/graphql/types'
import typeTitle from '@/util/type-title'

defineProps<{ wikibaseType: WikibaseType | null | undefined }>()
</script>

<template>
	<v-chip class="wikibase-type-chip" variant="outlined">
		{{ typeTitle(wikibaseType) }}
	</v-chip>
</template>

<style lang="css">
.wikibase-type-chip {
	border-radius: calc(0.625rem - 2px);
	padding: 0 8px !important;
	/* padding-block: 0.125rem; */
	border-color: oklch(87.2% 0.01 285.338);
	height: 30px !important;
}
.wikibase-type-chip .v-chip__content {
	font-family: Roboto;
	font-size: 16px;
	font-weight: 500;
}
</style>
