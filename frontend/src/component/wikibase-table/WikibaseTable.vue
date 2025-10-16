<script setup lang="ts">
import WikibaseTableRow from '@/component/wikibase-table/WikibaseTableRow.vue'
import type {
	WbFragment,
	WikibaseQuantityObservationWikibaseObservationSet as WikibaseQuantityObservationSet,
	WikibaseRecentChangesObservationWikibaseObservationSet as WikibaseRecentChangesObservationSet
} from '@/graphql/types'
import computeTotalEdits from '@/util/computeTotalEdits'
import { compareByValue } from '@/util/sortByValue'
import { ref } from 'vue'
import type { SortItem } from 'vuetify/lib/components/VDataTable/composables/sort.mjs'

const sortBy = ref<SortItem[]>([{ key: 'quantityObservations', order: 'desc' }])

const headers = [
	{ title: 'Type', value: 'wikibaseType', sortable: true },
	{ title: 'Title', value: 'title', sortable: true },
	{ title: 'URL', value: 'urls.baseUrl', sortable: true },
	{
		title: 'Triples',
		value: 'quantityObservations',
		sortable: true,
		sort: (a: WikibaseQuantityObservationSet, b: WikibaseQuantityObservationSet) =>
			compareByValue(a, b, (v) => v.mostRecent?.totalTriples)
	},
	{
		title: 'Edits',
		value: 'recentChangesObservations',
		sortable: true,
		sort: (a: WikibaseRecentChangesObservationSet, b: WikibaseRecentChangesObservationSet) =>
			compareByValue(a, b, computeTotalEdits)
	}
]

defineProps<{ error: boolean; loading: boolean; wikibases: WbFragment[] | undefined }>()
</script>

<template>
	<v-alert v-if="error" type="error" variant="tonal" title="Error">Error fetching data</v-alert>
	<v-data-table
		:items="wikibases"
		:headers="headers"
		striped="even"
		:loading="loading"
		v-model:sort-by="sortBy"
		class="wikibase-table"
	>
		<template v-slot:item="{ item }">
			<WikibaseTableRow :wikibase="item" />
		</template>
	</v-data-table>
</template>

<style lang="css"></style>
