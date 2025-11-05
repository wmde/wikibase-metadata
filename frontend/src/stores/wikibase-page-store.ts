import { pageWikibasesQuery } from '@/graphql/queries/wikibase-list-query'
import {
	WikibaseType,
	type PageWikibasesQuery,
	type PageWikibasesQueryVariables,
	type WikibaseFilterInput
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
	pageNumber: number
	// setPageNumber: (i: number) => void
	pageSize: number
	// setPageSize: (i: number) => void
	wikibaseFilter: WikibaseFilterInput
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
	// const setPageNumber = (i: number) => (pageNumber.value = i)

	const pageSize = ref(10000)
	// const setPageSize = (i: number) => (pageSize.value = i)
	watch(wikibasePage, () => {
		if (
			wikibasePage.value.data &&
			wikibasePage.value.data.wikibaseList.meta.totalCount > pageSize.value
		) {
			pageSize.value = wikibasePage.value.data.wikibaseList.meta.totalCount
		}
	})

	const wikibaseFilter = ref<WikibaseFilterInput>({
		wikibaseType: { include: [ WikibaseType.Cloud, WikibaseType.Suite,WikibaseType.Unknown] }
	})
	const includeWikibaseTypes = (t: WikibaseType[]) =>
		(wikibaseFilter.value = { ...wikibaseFilter.value, wikibaseType: { include: t } })

	const fetchWikibasePage = () =>
		load(pageWikibasesQuery, {
			pageNumber: pageNumber.value,
			pageSize: pageSize.value,
			wikibaseFilter: wikibaseFilter.value
		})
	watch(pageNumber, () => fetchWikibasePage())
	watch(pageSize, () => fetchWikibasePage())
	watch(wikibaseFilter, () => fetchWikibasePage())

	return {
		fetchWikibasePage,
		wikibasePage,
		pageNumber: pageNumber.value,
		// setPageNumber,
		pageSize: pageSize.value,
		// setPageSize,
		wikibaseFilter: wikibaseFilter.value,
		includeWikibaseTypes
	}
})
