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
import { computed, ref } from 'vue'

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

  const pageSize = 100
  const pageNumber = ref(1)
  const wikibaseFilter = ref<WikibaseFilterInput>({
    wikibaseType: { exclude: [WikibaseType.Test] }
  })
  const fetchWikibasePage = () =>
    load(pageWikibasesQuery, {
      pageNumber: pageNumber.value,
      pageSize,
      wikibaseFilter: wikibaseFilter.value
    })

  return { fetchWikibasePage, wikibasePage }
})
