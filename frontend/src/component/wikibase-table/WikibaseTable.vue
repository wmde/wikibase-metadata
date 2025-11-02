<script setup lang="ts">
import WikibaseTableRow from '@/component/wikibase-table/WikibaseTableRow.vue'
import type {
	WbFragment,
	WikibaseQuantityObservationWikibaseObservationSet as WikibaseQuantityObservationSet,
	WikibaseRecentChangesObservationWikibaseObservationSet as WikibaseRecentChangesObservationSet
} from '@/graphql/types'
import compareByValue from '@/util/compare-by-value'
import computeTotalEdits from '@/util/compute-total-edits'
import { ref } from 'vue'
import type { SortItem } from 'vuetify/lib/components/VDataTable/composables/sort.mjs'

const sortBy = ref<SortItem[]>([{ key: 'quantityObservations', order: 'desc' }])
const page = ref(1)
const itemsPerPage = ref(10)

const headers = [
	{ title: '', sortable: false },
	{ title: 'Type', value: 'wikibaseType', sortable: true },
	{ title: 'Title', value: 'title', sortable: true },
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
	},
	{ title: 'Category', value: 'category', sortable: true },
	{ title: 'Description', sortable: false },
	{ title: 'Details', value: 'id', sortable: false }
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
		v-model:page="page"
		v-model:items-per-page="itemsPerPage"
		class="wikibase-table"
	>
		<template v-slot:item="{ item, index }">
			<WikibaseTableRow :wikibase="item" :index="(page - 1) * itemsPerPage + index" />
		</template>
	</v-data-table>
</template>

<style lang="css"></style>
