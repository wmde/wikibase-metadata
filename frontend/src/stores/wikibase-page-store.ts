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
import { computed, ref, watch } from 'vue'

provideApolloClient(apolloClient)

const { load, onResult, loading, error } = useLazyQuery<
	PageWikibasesQuery,
	PageWikibasesQueryVariables
>(pageWikibasesQuery)

export const useWikiStore = defineStore('wiki-list', () => {
	const wikibasePageData = ref<PageWikibasesQuery>()
	onResult(({ data }) => (wikibasePageData.value = data))

	const wikibasePage = computed<QueryResult<PageWikibasesQuery | undefined>>(() => ({
		data: wikibasePageData.value,
		loading: loading.value,
		errorState: error.value ? true : false
	}))

	const pageNumber = ref(1)
	const setPageNumber = (i: number) => (pageNumber.value = i)

	const pageSize = ref(100)
	const setPageSize = (i: number) => (pageSize.value = i)
	watch(wikibasePageData, () => {
		if (
			wikibasePageData.value &&
			wikibasePageData.value.wikibaseList.meta.totalCount > pageSize.value
		) {
			pageSize.value = wikibasePageData.value.wikibaseList.meta.totalCount
		}
	})

	const wikibaseFilter = ref<WikibaseFilterInput>({
		wikibaseType: { exclude: [WikibaseType.Test] }
	})
	const excludeWikibaseTypes = (t: WikibaseType[]) =>
		(wikibaseFilter.value = { ...wikibaseFilter.value, wikibaseType: { exclude: t } })

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
		setPageNumber,
		pageSize: pageSize.value,
		setPageSize,
		wikibaseFilter: wikibaseFilter.value,
		excludeWikibaseTypes
	}
})
