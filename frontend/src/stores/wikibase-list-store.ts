import listWikibasesQuery from '@/graphql/queries/wikibase-list-query'
import type { ListWikibasesQuery, WbItemFragment } from '@/graphql/types'
import { apolloClient } from '@/stores/client'
import type { QueryResult } from '@/stores/query-result'
import { provideApolloClient, useLazyQuery } from '@vue/apollo-composable'
import { defineStore } from 'pinia'
import { computed, ref, type Ref } from 'vue'

provideApolloClient(apolloClient)

type WikibaseListData = { meta: { totalCount: number }; data: WbItemFragment[] }

export type WikibaseListStoreType = {
	fetchWikibaseList: () => void
	wikibaseList:
		QueryResult<WikibaseListData | undefined> | Ref<QueryResult<WikibaseListData | undefined>>
}

const { load, onResult, loading, error } = useLazyQuery<ListWikibasesQuery>(listWikibasesQuery)

export const useWikiListStore = defineStore('wiki-list', (): WikibaseListStoreType => {
	const data = ref<WikibaseListData | undefined>()
	onResult((result) => (data.value = result.data.wikibaseList))

	const wikibaseList = computed<QueryResult<WikibaseListData | undefined>>(() => ({
		data: data.value,
		loading: loading.value,
		errorState: error.value ? true : false
	}))

	const fetchWikibaseList = () => load(listWikibasesQuery)

	return { fetchWikibaseList, wikibaseList }
})
