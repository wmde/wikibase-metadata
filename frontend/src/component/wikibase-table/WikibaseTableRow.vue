<script setup lang="ts">
import LocaleNumber from '@/component/LocaleNumber.vue'
import WikibaseDetailCard from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCard.vue'
import type { WbFragment } from '@/graphql/types'
import computeTotalEdits from '@/util/computeTotalEdits'
import { ref } from 'vue'

defineProps<{ wikibase: WbFragment }>()

const openDialog = ref(false)
const toggleOpenDialog = () => (openDialog.value = !openDialog.value)
</script>

<template>
	<tr>
		<td>
			<v-chip class="wikibase-type-chip">{{ wikibase.wikibaseType }}</v-chip>
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
		<td>
			<v-btn v-on:click="toggleOpenDialog">VIEW</v-btn>
		</td>
	</tr>
	<v-dialog class="wikibase-detail-dialog" v-model="openDialog" width="auto">
		<WikibaseDetailCard :wikibase-id="Number.parseInt(wikibase.id)" />
	</v-dialog>
</template>

<style lang="css">
.wikibase-type-chip {
	min-width: 40px;
}
</style>
