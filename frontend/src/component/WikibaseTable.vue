<script setup lang="ts">
import LocaleNumber from '@/component/LocaleNumber.vue'
import type {
	WbFragment,
	WikibaseQuantityObservationWikibaseObservationSet as WikibaseQuantityObservationSet,
	WikibaseRecentChangesObservationWikibaseObservationSet as WikibaseRecentChangesObservationSet
} from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { compareByValue } from '@/util/sortByValue'
import { computed, ref } from 'vue'
import type { SortItem } from 'vuetify/lib/components/VDataTable/composables/sort.mjs'

const store = useWikiStore()

const loading = computed(() => store.wikibasePage.loading)
const wikibases = computed<WbFragment[] | undefined>(
	() => store.wikibasePage.data?.wikibaseList.data
)

const sortBy = ref<SortItem[]>([{ key: 'quantityObservations', order: 'asc' }])

const computeTotalEdits = (v: WikibaseRecentChangesObservationSet): number | undefined =>
	v.mostRecent?.botChangeCount != undefined || v.mostRecent?.humanChangeCount != undefined
		? (v.mostRecent?.botChangeCount ?? 0) + (v.mostRecent?.humanChangeCount ?? 0)
		: undefined
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
		<template v-slot:item.quantityObservations="{ value }">
			<td><LocaleNumber :stat="value.mostRecent?.totalTriples" /></td>
		</template>
		<template v-slot:item.recentChangesObservations="{ value }">
			<td><LocaleNumber :stat="computeTotalEdits(value)" /></td>
		</template>
	</v-data-table>
</template>

<style lang="css"></style>
