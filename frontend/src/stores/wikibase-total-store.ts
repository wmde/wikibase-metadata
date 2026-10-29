import totalWikibasesQuery from '@/graphql/queries/wikibase-total-query'
import type { TotalWikibasesQuery, TotalWikibasesQueryVariables } from '@/graphql/types'
import { apolloClient } from '@/stores/client'
import type { QueryResult } from '@/stores/query-result'
import computeTotalEdits from '@/util/compute-total-edits'
import { provideApolloClient, useLazyQuery } from '@vue/apollo-composable'
import { defineStore } from 'pinia'
import { computed, ref, type Ref } from 'vue'

provideApolloClient(apolloClient)

type WikibaseTotalData = {
	totalCount: number
	totalEdits: number | undefined
	totalTriples: number
}

export type WikibaseTotalStoreType = {
	fetchWikibaseTotal: () => void
	wikibaseTotal:
		QueryResult<WikibaseTotalData | undefined> | Ref<QueryResult<WikibaseTotalData | undefined>>
}

const { load, onResult, loading, error } = useLazyQuery<
	TotalWikibasesQuery,
	TotalWikibasesQueryVariables
>(totalWikibasesQuery)

export const useWikiTotalStore = defineStore('wiki-total', (): WikibaseTotalStoreType => {
	const data = ref<WikibaseTotalData | undefined>()
	onResult(
		(result) =>
			(data.value = {
				totalCount: result.data.wikibaseList.meta.totalCount,
				totalEdits: computeTotalEdits(result.data.aggregateRecentChanges),
				totalTriples: result.data.aggregateQuantity.totalTriples
			})
	)

	const wikibaseTotal = computed<QueryResult<WikibaseTotalData | undefined>>(() => ({
		data: data.value,
		loading: loading.value,
		errorState: error.value ? true : false
	}))

	const fetchWikibaseTotal = () => load(totalWikibasesQuery)

	return { fetchWikibaseTotal, wikibaseTotal }
})
