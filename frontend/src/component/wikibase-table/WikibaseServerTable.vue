<script setup lang="ts">
import WikibaseTableRow from '@/component/wikibase-table/WikibaseTableRow.vue'
import { SortColumn, SortDirection, type WbFragment } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed, ref, watch } from 'vue'
import type { SortItem } from 'vuetify/lib/components/VDataTable/composables/sort.mjs'

type TableHeaderValue = 'wikibaseType' | 'title' | 'triples' | 'edits' | 'category'
type TableHeader = {
	title: string
	value?: TableHeaderValue
	sortable: boolean
}

const headers: TableHeader[] = [
	{ title: '', sortable: false },
	{ title: 'Type', value: 'wikibaseType', sortable: true },
	{ title: 'Title', value: 'title', sortable: true },
	{ title: 'Triples', value: 'triples', sortable: true },
	{ title: 'Edits', value: 'edits', sortable: true },
	{ title: 'Category', value: 'category', sortable: true },
	{ title: 'Description', sortable: false },
	{ title: 'Details', sortable: false }
]

const headerValueToColumn = (val: TableHeaderValue): SortColumn => {
	switch (val) {
		case 'category':
			return SortColumn.Category
		case 'edits':
			return SortColumn.Edits
		case 'title':
			return SortColumn.Title
		case 'triples':
			return SortColumn.Triples
		case 'wikibaseType':
			return SortColumn.Type
	}
}

const store = useWikiStore()

const pageNumber = ref(store.pageNumber)
watch(pageNumber, store.setPageNumber)

const pageSize = ref(store.pageSize)
watch(pageSize, store.setPageSize)

const sortBy = ref<SortItem[]>([{ key: 'triples', order: 'desc' }])
watch(sortBy, () =>
	store.setSort(
		sortBy.value[0]
			? {
					column: headerValueToColumn(sortBy.value[0].key as TableHeaderValue),
					dir: sortBy.value[0].order == 'asc' ? SortDirection.Asc : SortDirection.Desc
				}
			: undefined
	)
)

const error = computed(() => store.wikibasePage.errorState)
const loading = computed(() => store.wikibasePage.loading)

const totalCount = computed(() => store.wikibasePage.data?.wikibaseList.meta.totalCount)
const wikibases = computed<WbFragment[] | undefined>(
	() => store.wikibasePage.data?.wikibaseList.data
)
</script>

<template>
	<v-alert v-if="error" type="error" variant="tonal" title="Error">Error fetching data</v-alert>
	<p>Page: {{ pageNumber }}, {{ store.pageNumber }}</p>
	<p>Page Size: {{ pageSize }}, {{ store.pageSize }}</p>
	<p>Sort: {{ sortBy }}, {{ store.sortBy }}</p>
	<v-data-table-server
		v-model:items-per-page="pageSize"
		v-model:page="pageNumber"
		v-model:sort-by="sortBy"
		:headers="headers"
		:items="wikibases"
		:items-length="totalCount ?? 0"
		:loading="loading"
		striped="even"
		class="wikibase-table"
	>
		<template v-slot:item="{ item, index }">
			<WikibaseTableRow :wikibase="item" :index="(pageNumber - 1) * pageSize + index" />
		</template>
	</v-data-table-server>
</template>

<style lang="css"></style>
