<script setup lang="ts">
import WikibaseTableRow from '@/component/wikibase-table/WikibaseTableRow.vue'
import { SortColumn, SortDirection, type WbFragment } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed } from 'vue'
import type { SortItem } from 'vuetify/lib/components/VDataTable/composables/sort.mjs'

type TableHeader = { title: string; value?: SortColumn; sortable: boolean }

const headers: TableHeader[] = [
	{ title: '', sortable: false },
	// TODO: Fix Type sorting in Postgres
	{ title: 'Type', value: SortColumn.Type, sortable: false },
	{ title: 'Title', value: SortColumn.Title, sortable: true },
	{ title: 'Triples', value: SortColumn.Triples, sortable: true },
	{ title: 'Edits (last 30 days)', value: SortColumn.Edits, sortable: true },
	{ title: 'Category', value: SortColumn.Category, sortable: true },
	{ title: 'Description', sortable: false },
	{ title: 'Details', sortable: false }
]

const store = useWikiStore()

const loading = computed(() => store.wikibasePage.loading)
const pageNumber = computed(() => store.pageNumber)
const pageSize = computed(() => store.pageSize)
const sortBy = computed<SortItem[]>((): SortItem[] =>
	store.sortBy
		? [{ key: store.sortBy.column, order: store.sortBy.dir == SortDirection.Asc ? 'asc' : 'desc' }]
		: []
)
const totalCount = computed(() => store.wikibasePage.data?.meta.totalCount)
const wikibases = computed<WbFragment[] | undefined>(() =>
	store.wikibasePage.loading ? undefined : store.wikibasePage.data?.data
)
</script>

<template>
	<v-data-table-server
		:page="pageNumber"
		@update:page="store.setPageNumber"
		:items-per-page="pageSize"
		@update:items-per-page="store.setPageSize"
		:sort-by="sortBy"
		@update:sort-by="
			(sortBy: SortItem[]) =>
				store.setSort(
					sortBy[0]
						? {
								column: sortBy[0].key as SortColumn,
								dir: sortBy[0].order == 'asc' ? SortDirection.Asc : SortDirection.Desc
							}
						: undefined
				)
		"
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
