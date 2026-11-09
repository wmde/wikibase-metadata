<script setup lang="ts">
import WikibaseItemList from '@/component/wikibase-item-list/WikibaseItemList.vue'
import WikibaseSearch from '@/component/wikibase-table/WikibaseSearch.vue'
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import WikibaseTotalContainer from '@/component/wikibase-table/WikibaseTotalContainer.vue'
import { SEARCH_PARAM_NAME, useSearchStore } from '@/stores/search-store'
import { useWikiPageStore } from '@/stores/wikibase-page-store'
import { getUrlParamValue } from '@/util/use-url'
import { computed, onBeforeMount, onMounted } from 'vue'

const store = useWikiPageStore()
const showCount = computed(() => store.wikibasePage.data?.data.length)
const totalCount = computed(() => store.wikibasePage.data?.meta.totalCount)

const error = computed(() => store.wikibasePage.errorState)

const searchStore = useSearchStore()
const menuValue = computed(() => searchStore.menuValue)

onBeforeMount(() => store.fetchWikibasePage())
onMounted(() => searchStore.setSearchValue(getUrlParamValue(SEARCH_PARAM_NAME) ?? ''))
</script>

<template>
	<v-container class="wikibase-table-container my-0 px-6 py-8">
		<v-alert v-if="error" type="error" variant="tonal" title="Error">Error fetching data</v-alert>
		<wikibase-total-container />
		<wikibase-search />
		<template v-if="menuValue == 'instances'">
			<v-container v-if="totalCount && showCount" class="show-count mb-6 pa-0">
				Showing {{ showCount.toLocaleString('en') }} of
				{{ totalCount.toLocaleString('en') }} instances
			</v-container>
			<wikibase-table />
		</template>
		<template v-if="menuValue == 'items'">
			<wikibase-item-list />
		</template>
	</v-container>
</template>

<style lang="css">
.show-count {
	font-family: Roboto;
	font-size: 16px;
	color: #000;
}
</style>
