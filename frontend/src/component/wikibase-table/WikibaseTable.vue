<script setup lang="ts">
import type {
	WbFragment,
	WikibaseQuantityObservationWikibaseObservationSet as WikibaseQuantityObservationSet,
	WikibaseRecentChangesObservationWikibaseObservationSet as WikibaseRecentChangesObservationSet
} from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import computeTotalEdits from '@/util/computeTotalEdits'
import { compareByValue } from '@/util/sortByValue'
import { computed, ref } from 'vue'
import type { SortItem } from 'vuetify/lib/components/VDataTable/composables/sort.mjs'
import WikibaseTableRow from './WikibaseTableRow.vue'

const store = useWikiStore()

const loading = computed(() => store.wikibasePage.loading)
const wikibases = computed<WbFragment[] | undefined>(
	() => store.wikibasePage.data?.wikibaseList.data
)

const sortBy = ref<SortItem[]>([{ key: 'quantityObservations', order: 'asc' }])

const headers = [
	{ title: 'Type', value: 'wikibaseType', sortable: true },
	{ title: 'Title', value: 'title', sortable: true },
	{ title: 'URL', value: 'urls.baseUrl', sortable: true },
	{
		title: 'Triples',
		value: 'quantityObservations',
		sortable: true,
		sort: (a: WikibaseQuantityObservationSet, b: WikibaseQuantityObservationSet) =>
			compareByValue(a, b, (v) => v.mostRecent?.totalTriples) * -1
	},
	{
		title: 'Edits',
		value: 'recentChangesObservations',
		sortable: true,
		sort: (a: WikibaseRecentChangesObservationSet, b: WikibaseRecentChangesObservationSet) =>
			compareByValue(a, b, computeTotalEdits) * -1
	}
]
</script>

<template>
	<v-data-table
		:items="wikibases"
		:headers="headers"
		striped="even"
		:loading="loading"
		v-model:sort-by="sortBy"
	>
		<template v-slot:item="{ item }">
			<WikibaseTableRow :wikibase="item" />
		</template>
	</v-data-table>
</template>

<style lang="css"></style>
