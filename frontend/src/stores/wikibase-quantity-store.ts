import allQuantityWikibasesQuery from '@/graphql/queries/wikibase-quantity-query'
import {
	WikibaseType,
	type AllQuantityWikibasesQuery,
	type AllQuantityWikibasesQueryVariables,
	type WbQuantityFragment,
	type WikibaseFilterInput
} from '@/graphql/types'
import { apolloClient } from '@/stores/client'
import type { QueryResult } from '@/stores/query-result'
import { provideApolloClient, useLazyQuery } from '@vue/apollo-composable'
import { defineStore } from 'pinia'
import { computed, ref, watch, type Ref } from 'vue'

provideApolloClient(apolloClient)

export type WikibaseQuantityStoreType = {
	fetchWikibases: () => void
	wikibases:
		| QueryResult<WbQuantityFragment[] | undefined>
		| Ref<QueryResult<WbQuantityFragment[] | undefined>>
	wikibaseFilter: WikibaseFilterInput | Ref<WikibaseFilterInput>
	includeWikibaseTypes: (t: WikibaseType[]) => void
	searchWikibaseText: (s: string | undefined) => void
}

const { load, onResult, loading, error } = useLazyQuery<
	AllQuantityWikibasesQuery,
	AllQuantityWikibasesQueryVariables
>(allQuantityWikibasesQuery)

export const useWikiQuantityStore = defineStore(
	'wiki-quantity-list',
	(): WikibaseQuantityStoreType => {
		const data = ref<WbQuantityFragment[] | undefined>()
		onResult(
			(result) =>
				(data.value = result.data.wikibaseList.data.filter(
					(w) => w.quantityObservations.allObservations.filter((q) => q.returnedData).length > 0
				))
		)

		const wikibases = computed<QueryResult<WbQuantityFragment[] | undefined>>(() => ({
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

		const fetchWikibases = () =>
			load(allQuantityWikibasesQuery, { wikibaseFilter: wikibaseFilter.value })
		watch(wikibaseFilter, fetchWikibases)

		return { fetchWikibases, wikibases, wikibaseFilter, includeWikibaseTypes, searchWikibaseText }
	}
)
