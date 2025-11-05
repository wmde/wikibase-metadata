import pageWikibasesQuery from '@/graphql/queries/wikibase-page-query'
import {
	SortColumn,
	SortDirection,
	WikibaseType,
	type PageWikibasesQuery,
	type PageWikibasesQueryVariables,
	type WbFragment,
	type WikibaseFilterInput,
	type WikibaseSortInput
} from '@/graphql/types'
import { apolloClient } from '@/stores/client'
import type { QueryResult } from '@/stores/query-result'
import { provideApolloClient, useLazyQuery } from '@vue/apollo-composable'
import { defineStore } from 'pinia'
import { computed, ref, watch, type Ref } from 'vue'

provideApolloClient(apolloClient)

type WikibasePageData = { meta: { totalCount: number }; data: WbFragment[] }

export type WikibasePageStoreType = {
	fetchWikibasePage: () => void
	wikibasePage:
		| QueryResult<WikibasePageData | undefined>
		| Ref<QueryResult<WikibasePageData | undefined>>
	pageNumber: number | Ref<number>
	setPageNumber: (i: number) => void
	pageSize: number | Ref<number>
	setPageSize: (i: number) => void
	sortBy: WikibaseSortInput | undefined | Ref<WikibaseSortInput | undefined>
	setSort: (sortBy: WikibaseSortInput | undefined) => void
	wikibaseFilter: WikibaseFilterInput | Ref<WikibaseFilterInput>
	includeWikibaseTypes: (t: WikibaseType[]) => void
}

const { load, onResult, loading, error } = useLazyQuery<
	PageWikibasesQuery,
	PageWikibasesQueryVariables
>(pageWikibasesQuery)

export const useWikiStore = defineStore('wiki-list', (): WikibasePageStoreType => {
	const data = ref<WikibasePageData | undefined>()
	onResult((result) => (data.value = result.data.wikibaseList))

	const wikibasePage = computed<QueryResult<WikibasePageData | undefined>>(() => ({
		data: data.value,
		loading: loading.value,
		errorState: error.value ? true : false
	}))

	const pageNumber = ref(1)
	const setPageNumber = (i: number) => (pageNumber.value = i)

	const pageSize = ref(10)
	const setPageSize = (i: number) => (pageSize.value = i)
	watch(pageSize, () => setPageNumber(1))

	const sortBy = ref<WikibaseSortInput | undefined>({
		column: SortColumn.Triples,
		dir: SortDirection.Desc
	})
	const setSort = (val: WikibaseSortInput | undefined) => (sortBy.value = val)
	watch(sortBy, () => setPageNumber(1))

	const wikibaseFilter = ref<WikibaseFilterInput>({
		wikibaseType: { include: [WikibaseType.Cloud, WikibaseType.Suite, WikibaseType.Unknown] }
	})
	const includeWikibaseTypes = (t: WikibaseType[]) =>
		(wikibaseFilter.value = { ...wikibaseFilter.value, wikibaseType: { include: t } })
	watch(wikibaseFilter, () => setPageNumber(1))

	const fetchWikibasePage = () =>
		load(pageWikibasesQuery, {
			pageNumber: pageNumber.value,
			pageSize: pageSize.value,
			sortBy: sortBy.value,
			wikibaseFilter: wikibaseFilter.value
		})
	watch(pageNumber, fetchWikibasePage)
	watch(pageSize, fetchWikibasePage)
	watch(sortBy, fetchWikibasePage)
	watch(wikibaseFilter, fetchWikibasePage)

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
