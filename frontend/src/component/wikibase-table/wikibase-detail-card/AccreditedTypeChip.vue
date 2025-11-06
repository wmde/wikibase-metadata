<script setup lang="ts">
import WikibaseTypeChip from '@/component/wikibase-table/WikibaseTypeChip.vue'
import { WikibaseType, type SingleWikibaseFragment } from '@/graphql/types'

defineProps<{ wikibase: SingleWikibaseFragment }>()
</script>

<template>
	<v-tooltip
		class="type-tooltip"
		:text="
			wikibase.wikibaseType == WikibaseType.Cloud
				? `Automatically pulled from Cloud API`
				: wikibase.wikibaseType == undefined
					? `Not set`
					: `Manually set`
		"
	>
		<template v-slot:activator="{ props }">
			<WikibaseTypeChip :wikibase-type="wikibase.wikibaseType" v-bind="props" />
		</template>
	</v-tooltip>
</template>
