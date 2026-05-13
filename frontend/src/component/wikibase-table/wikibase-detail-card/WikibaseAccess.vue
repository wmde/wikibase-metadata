<script setup lang="ts">
import type { SingleWikibaseFragment } from '@/graphql/types'
import { mdiLink, mdiMagnify } from '@mdi/js'

defineProps<{ wikibase: SingleWikibaseFragment }>()
</script>

<template>
	<v-container class="ma-0 pa-0 access-container">
		<v-container class="ma-0 mb-4 pa-0 title">Access</v-container>
		<v-container class="ma-0 pa-0 acc-container">
			<v-btn
				:prepend-icon="mdiLink"
				size="large"
				variant="outlined"
				:href="wikibase.urls.baseUrl"
				target="_blank"
			>
				Visit Instance
			</v-btn>
			<v-btn
				v-if="wikibase.urls.sparqlFrontendUrl"
				:prepend-icon="mdiMagnify"
				size="large"
				variant="outlined"
				:href="wikibase.urls.sparqlFrontendUrl"
				target="_blank"
			>
				Query Service
			</v-btn>
		</v-container>
	</v-container>
</template>

<style lang="css">
.acc-container {
	display: flex;
	flex-flow: column nowrap;
	gap: 0.75rem;
}
.acc-container a {
	display: flex;
	justify-content: flex-start;
	text-transform: none;
	color: rgb(54, 40, 245);
	border-color: rgb(54, 40, 245);
	gap: 0.75rem;
}
.access-container .title {
	font-family: Montserrat;
	font-weight: 700;
	font-size: 20px;
	color: rgb(0, 0, 0);
}
</style>
