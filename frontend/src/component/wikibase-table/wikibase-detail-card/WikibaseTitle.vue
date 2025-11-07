<script setup lang="ts">
import { WikibaseType, type SingleWikibaseFragment } from '@/graphql/types'

defineProps<{ wikibase: SingleWikibaseFragment }>()
</script>

<template>
	<v-container class="wikibase-url wikibase-title ma-0 pa-0">
		<v-tooltip
			class="base-url-tooltip"
			:text="
				wikibase.wikibaseType == WikibaseType.Cloud
					? `Automatically pulled from Cloud API`
					: `Manually set`
			"
		>
			<template v-slot:activator="{ props }">
				<a v-bind="props" :href="wikibase.urls.baseUrl">
					{{ wikibase.title }}
				</a>
			</template>
		</v-tooltip>
	</v-container>
</template>
