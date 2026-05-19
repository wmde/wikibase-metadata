<script setup lang="ts">
import type { SingleWikibaseFragment } from '@/graphql/types'

defineProps<{ wikibase: SingleWikibaseFragment }>()
</script>

<template>
	<v-container class="wikibase-url wikibase-title mx-0 pa-0">
		{{ wikibase.title }}
	</v-container>
</template>

<style lang="css" scoped>
.wikibase-title {
	font-family: Montserrat;
	font-weight: 700;
	font-size: 28px;
	color: #000;
	margin-top: 0;
	margin-bottom: 16px;
	line-height: 1;
}
</style>
