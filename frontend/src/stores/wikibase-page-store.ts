import { pageWikibasesQuery } from '@/graphql/queries/wikibase-list-query'
import {
	SortColumn,
	SortDirection,
	WikibaseType,
	type PageWikibasesQuery,
	type PageWikibasesQueryVariables,
	type WikibaseFilterInput,
	type WikibaseSortInput
} from '@/graphql/types'
import { apolloClient } from '@/stores/client'
import type { QueryResult } from '@/stores/query-result'
import { provideApolloClient, useLazyQuery } from '@vue/apollo-composable'
import { defineStore } from 'pinia'
import { computed, ref, watch, type Ref } from 'vue'

provideApolloClient(apolloClient)

export type WikibasePageStoreType = {
	fetchWikibasePage: () => void
	wikibasePage:
		| QueryResult<PageWikibasesQuery | undefined>
		| Ref<QueryResult<PageWikibasesQuery | undefined>>
	pageNumber: number | Ref<number>
	setPageNumber: (i: number) => void
	pageSize: number | Ref<number>
	setPageSize: (i: number) => void
	sortBy: WikibaseSortInput | undefined | Ref<WikibaseSortInput | undefined>
	setSort: (sortBy: WikibaseSortInput | undefined) => void
	wikibaseFilter: WikibaseFilterInput | Ref<WikibaseFilterInput>
	includeWikibaseTypes: (t: WikibaseType[]) => void
}

const { load, result, loading, error } = useLazyQuery<
	PageWikibasesQuery,
	PageWikibasesQueryVariables
>(pageWikibasesQuery)

export const useWikiStore = defineStore('wiki-list', (): WikibasePageStoreType => {
	const wikibasePage = computed<QueryResult<PageWikibasesQuery | undefined>>(() => ({
		data: result.value,
		loading: loading.value,
		errorState: error.value ? true : false
	}))

	const pageNumber = ref(1)
	const setPageNumber = (i: number) => (pageNumber.value = i)

	const pageSize = ref(10)
	const setPageSize = (i: number) => (pageSize.value = i)

	const sortBy = ref<WikibaseSortInput | undefined>({
		column: SortColumn.Triples,
		dir: SortDirection.Desc
	})
	const setSort = (val: WikibaseSortInput | undefined) => (sortBy.value = val)

	const wikibaseFilter = ref<WikibaseFilterInput>({
		wikibaseType: { include: [WikibaseType.Cloud, WikibaseType.Suite, WikibaseType.Unknown] }
	})
	const includeWikibaseTypes = (t: WikibaseType[]) =>
		(wikibaseFilter.value = { ...wikibaseFilter.value, wikibaseType: { include: t } })

	const fetchWikibasePage = () =>
		load(pageWikibasesQuery, {
			pageNumber: pageNumber.value,
			pageSize: pageSize.value,
			sortBy: sortBy.value,
			wikibaseFilter: wikibaseFilter.value
		})
	watch(pageNumber, () => fetchWikibasePage())
	watch(pageSize, () => fetchWikibasePage())
	watch(sortBy, () => fetchWikibasePage())
	watch(wikibaseFilter, () => fetchWikibasePage())

	return {
		fetchWikibasePage,
		wikibasePage,
		pageNumber,
		setPageNumber,
		pageSize,
		setPageSize,
		sortBy,
		setSort,
		wikibaseFilter,
		includeWikibaseTypes
	}
})
