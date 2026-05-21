<script setup lang="ts">
import type { SingleWikibaseFragment } from '@/graphql/types'
import { computed } from 'vue'
import { mdiLink, mdiMagnify } from '@mdi/js'
import { FileBox } from 'lucide-vue-next'

const { wikibase } = defineProps<{ wikibase: SingleWikibaseFragment }>()

const actionApiUrl = computed(() => {
	const scriptPath = wikibase.urls.scriptPath

	if (!scriptPath) {
		return null
	}

	const base = wikibase.urls.baseUrl.replace(/\/$/, '')
	const s = '/' + scriptPath.replace(/^\/|\/$/g, '') // remove leading and trailing slashes
	return `${base}${s}/api.php`
})
</script>

<template>
	<v-container class="ma-0 pa-0 pb-8 access-container">
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
			<v-btn
				v-if="actionApiUrl"
				:prepend-icon="FileBox"
				size="large"
				variant="outlined"
				:href="actionApiUrl"
				target="_blank"
				id="api-button"
			>
				API
			</v-btn>
		</v-container>
	</v-container>
</template>

<style lang="scss">
.access-container {
	.acc-container {
		display: flex;
		flex-flow: column nowrap;
		gap: 0.75rem;
		a {
			display: flex;
			justify-content: flex-start;
			text-transform: none;
			color: rgb(54, 40, 245);
			border-color: rgb(54, 40, 245);
			gap: 0.75rem;
		}
	}
	.title {
		font-family: Montserrat;
		font-weight: 700;
		font-size: 20px;
		color: rgb(0, 0, 0);
	}
}
</style>
