<script setup lang="ts">
import LocaleNumber from '@/component/LocaleNumber.vue'
import type { WbFragment } from '@/graphql/types'
import computeTotalEdits from '@/util/computeTotalEdits'
import { ref } from 'vue'

defineProps<{ wikibase: WbFragment }>()

const openDialog = ref(false)
const toggleOpenDialog = () => (openDialog.value = !openDialog.value)
</script>

<template>
	<tr v-on:click="toggleOpenDialog">
		<td>
			{{ wikibase.wikibaseType }}
			{{ openDialog }}
		</td>
		<td>
			{{ wikibase.title }}
		</td>
		<td>
			{{ wikibase.urls.baseUrl }}
		</td>
		<td>
			<LocaleNumber :stat="wikibase.quantityObservations.mostRecent?.totalTriples" />
		</td>
		<td>
			<LocaleNumber :stat="computeTotalEdits(wikibase.recentChangesObservations)" />
		</td>
	</tr>
	<v-dialog v-model="openDialog" width="auto">
		<v-card :max-width="500">
			{{ wikibase }}
		</v-card>
	</v-dialog>
</template>

<style lang="css"></style>
