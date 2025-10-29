<script setup lang="ts">
import WikibaseTableRow from '@/component/wikibase-table/WikibaseTableRow.vue'
import type { WbFragment } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed, ref } from 'vue'
import type { SortItem } from 'vuetify/lib/components/VDataTable/composables/sort.mjs'

const store = useWikiStore()

const sortBy = ref<SortItem[]>([{ key: 'quantityObservations', order: 'desc' }])
const page = computed(() => store.pageNumber)
const itemsPerPage = computed(() => store.pageSize)
const updatePageCount = (items: number) => store.setPageSize(items)
const updatePageNumber = (page: number) => store.setPageNumber(page)

const error = computed(() => store.wikibasePage.errorState)
const loading = computed(() => store.wikibasePage.loading)

const totalCount = computed(() => store.wikibasePage.data?.wikibaseList.meta.totalCount)
const wikibases = computed<WbFragment[] | undefined>(
	() => store.wikibasePage.data?.wikibaseList.data
)
const headers = [
	{ title: '', sortable: false },
	{ title: 'Type', value: 'wikibaseType', sortable: true },
	{ title: 'Title', value: 'title', sortable: true },
	{
		title: 'Triples',
		value: 'quantityObservations',
		sortable: true
	},
	{
		title: 'Edits',
		value: 'recentChangesObservations',
		sortable: true
	},
	{ title: 'Category', value: 'category', sortable: true },
	{ title: 'Description', sortable: false },
	{ title: 'Details', value: 'id', sortable: false }
]
</script>

<template>
	<v-alert v-if="error" type="error" variant="tonal" title="Error">Error fetching data</v-alert>
	<p>Page: {{ page }}, {{ store.pageNumber }}</p>
	<p>Page Size: {{ itemsPerPage }}, {{ store.pageSize }}</p>
	<p>Sort: {{ sortBy }}</p>
	<v-data-table-server
		v-model:items-per-page="itemsPerPage"
		v-model:page="page"
		v-model:sort-by="sortBy"
		:headers="headers"
		:items="wikibases"
		:items-length="totalCount ?? 0"
		:loading="loading"
		@update:items-per-page="updatePageCount"
		@update:page="updatePageNumber"
		striped="even"
		class="wikibase-table"
	>
		<template v-slot:item="{ item, index }">
			<WikibaseTableRow :wikibase="item" :index="(page - 1) * itemsPerPage + index" />
		</template>
	</v-data-table-server>
</template>

<style lang="css"></style>
