<script setup lang="ts">
import type { SingleWikibaseFragment } from '@/graphql/types'

defineProps<{ wikibase: SingleWikibaseFragment }>()
</script>

<template>
	<v-container class="description ma-0 pa-0">
		{{ wikibase.description }}
	</v-container>
</template>
<style lang="css">
.description {
	font-family: Roboto;
	font-size: 16px;
	color: rgb(0, 0, 0);
	line-height: 1.6;
}
</style>
