import allTTFVWikibasesQuery from '@/graphql/queries/wikibase-ttfv-query'
import {
	WikibaseType,
	type AllTtfvWikibasesQuery,
	type AllTtfvWikibasesQueryVariables,
	type WbttfvFragment,
	type WikibaseFilterInput
} from '@/graphql/types'
import { apolloClient } from '@/stores/client'
import type { QueryResult } from '@/stores/query-result'
import { provideApolloClient, useLazyQuery } from '@vue/apollo-composable'
import { defineStore } from 'pinia'
import { computed, ref, watch, type Ref } from 'vue'

provideApolloClient(apolloClient)

export type WikibaseTTFVStoreType = {
	fetchWikibases: () => void
	wikibases:
		| QueryResult<WbttfvFragment[] | undefined>
		| Ref<QueryResult<WbttfvFragment[] | undefined>>
	wikibaseFilter: WikibaseFilterInput | Ref<WikibaseFilterInput>
	includeWikibaseTypes: (t: WikibaseType[]) => void
	searchWikibaseText: (s: string | undefined) => void
}

const { load, onResult, loading, error } = useLazyQuery<
	AllTtfvWikibasesQuery,
	AllTtfvWikibasesQueryVariables
>(allTTFVWikibasesQuery)

export const useWikiTTFVStore = defineStore('wiki-ttfv-list', (): WikibaseTTFVStoreType => {
	const data = ref<WbttfvFragment[] | undefined>()
	onResult((result) => (data.value = result.data.wikibaseList.data))

	const wikibases = computed<QueryResult<WbttfvFragment[] | undefined>>(() => ({
		data: data.value,
		loading: loading.value,
		errorState: error.value ? true : false
	}))

	const wikibaseFilter = ref<WikibaseFilterInput>({
		wikibaseType: { include: [WikibaseType.Cloud, WikibaseType.Suite, WikibaseType.Unknown] }
	})
	const includeWikibaseTypes = (t: WikibaseType[]) =>
		(wikibaseFilter.value = { ...wikibaseFilter.value, wikibaseType: { include: t } })
	const searchWikibaseText = (s: string | undefined) =>
		(wikibaseFilter.value = { ...wikibaseFilter.value, searchText: s })

	const fetchWikibases = () => load(allTTFVWikibasesQuery, { wikibaseFilter: wikibaseFilter.value })
	watch(wikibaseFilter, fetchWikibases)

	return { fetchWikibases, wikibases, wikibaseFilter, includeWikibaseTypes, searchWikibaseText }
})
