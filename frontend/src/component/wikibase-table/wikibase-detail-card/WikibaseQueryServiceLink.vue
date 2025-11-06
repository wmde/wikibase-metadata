<script setup lang="ts">
import { WikibaseType, type SingleWikibaseFragment } from '@/graphql/types'

defineProps<{ wikibase: SingleWikibaseFragment }>()
</script>

<template>
	<v-container v-if="wikibase.urls.sparqlFrontendUrl" class="wikibase-url ma-0 pa-0">
		<v-tooltip
			class="sparql-url-tooltip"
			:text="
				wikibase.wikibaseType == WikibaseType.Cloud
					? `Automatically pulled from Cloud API`
					: `Manually set`
			"
		>
			<template v-slot:activator="{ props }">
				<a v-bind="props" :href="wikibase.urls.sparqlFrontendUrl">Query Service</a>
			</template>
		</v-tooltip>
	</v-container>
</template>
