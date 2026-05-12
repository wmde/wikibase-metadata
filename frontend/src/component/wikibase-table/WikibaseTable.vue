<script setup lang="ts">
import WikibaseTableRow from '@/component/wikibase-table/WikibaseTableRow.vue'
import { SortColumn, SortDirection, type WbFragment } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { mdiSwapVertical } from '@mdi/js'
import { computed } from 'vue'
import type { SortItem } from 'vuetify/lib/components/VDataTable/composables/sort.mjs'

type TableHeader = { title: string; value?: SortColumn; sortable: boolean }

const headers: TableHeader[] = [
	{ title: 'Title', value: SortColumn.Title, sortable: true },
	{ title: 'Triples', value: SortColumn.Triples, sortable: true },
	{ title: 'Edits', value: SortColumn.Edits, sortable: true },
	{ title: 'Category', value: SortColumn.Category, sortable: true },
	{ title: 'Description', sortable: false },
	{ title: '', sortable: false }
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
		:items-per-page-options="[
			{ value: 25, title: '25' },
			{ value: 50, title: '50' },
			{ value: 100, title: '100' },
			{ value: -1, title: '$vuetify.dataFooter.itemsPerPageAll' }
		]"
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
		class="wikibase-table"
	>
		<template v-slot:headers="{ columns, isSorted, getSortIcon, toggleSort }">
			<tr class="table-header-row">
				<template v-for="(column, idx) in columns" :key="idx">
					<th :class="'table-header-cell' + column.sortable ? ' v-data-table__th--sortable' : ''">
						<div class="d-flex align-center">
							<span class="me-2 cursor-pointer table-header-cell-title" @click="toggleSort(column)">
								{{ column.title }}
							</span>
							<v-icon
								v-if="column.sortable"
								:icon="isSorted(column) ? getSortIcon(column) : mdiSwapVertical"
								color="medium-emphasis"
							/>
						</div>
						<span class="table-header-cell-subtitle" v-if="column.title == 'Edits'"
							>(last 30 days)</span
						>
					</th>
				</template>
			</tr>
		</template>
		<template v-slot:item="{ item, index }">
			<WikibaseTableRow :wikibase="item" :index="(pageNumber - 1) * pageSize + index" />
		</template>
	</v-data-table-server>
</template>

<style lang="css">
.table-header-row {
	background-color: oklch(98.5% 0.002 247.839);
}
.table-header-cell {
	font-family: Montserrat;
	color: rgb(0, 0, 0);
}
.table-header-cell-title {
	font-weight: 700 !important;
	font-size: 16px;
}
.table-header-cell-subtitle {
	font-size: 14px;
	font-weight: 400 !important;
}
</style>
