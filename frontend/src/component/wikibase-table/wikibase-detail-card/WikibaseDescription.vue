<script setup lang="ts">
import type { SingleWikibaseFragment } from '@/graphql/types'

defineProps<{ wikibase: SingleWikibaseFragment }>()
</script>

<template>
	<v-tooltip v-if="wikibase.description" class="desc-tooltip" text="Manually written">
		<template v-slot:activator="{ props }">
			<v-container v-bind="props" class="description ma-0 pa-0">
				{{ wikibase.description }}
			</v-container>
		</template>
	</v-tooltip>
</template>
