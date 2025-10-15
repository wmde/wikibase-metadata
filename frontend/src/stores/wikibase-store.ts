import { singleWikibaseQuery } from '@/graphql/queries/single-wikibase-query'
import { type SingleWikibaseQuery, type SingleWikibaseQueryVariables } from '@/graphql/types'
import { apolloClient } from '@/stores/client'
import type { QueryResult } from '@/stores/query-result'
import { provideApolloClient, useLazyQuery } from '@vue/apollo-composable'
import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'

provideApolloClient(apolloClient)

const { load, result, loading, error } = useLazyQuery<
	SingleWikibaseQuery,
	SingleWikibaseQueryVariables
>(singleWikibaseQuery)

export const useSingleWikiStore = defineStore('single-wiki', () => {
	const wikibase = computed<QueryResult<SingleWikibaseQuery | null>>(() => ({
		data: result.value ?? null,
		loading: loading.value,
		errorState: error.value ? true : false
	}))

	const wikibaseId = ref<number>()
	const searchWikibase = (i: number) => (wikibaseId.value = i)

	const fetchWikibase = () =>
		wikibaseId.value && load(singleWikibaseQuery, { wikibaseId: wikibaseId.value })
	watch(wikibaseId, () => fetchWikibase())

	return { fetchWikibase, wikibaseId, wikibase, searchWikibase }
})
