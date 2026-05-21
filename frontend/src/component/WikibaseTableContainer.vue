<script setup lang="ts">
import WikibaseSearch from '@/component/wikibase-table/WikibaseSearch.vue'
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import WikibaseTotalContainer from '@/component/wikibase-table/WikibaseTotalContainer.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed, onBeforeMount } from 'vue'

const store = useWikiStore()
const showCount = computed(() => store.wikibasePage.data?.data.length)
const totalCount = computed(() => store.wikibasePage.data?.meta.totalCount)

const error = computed(() => store.wikibasePage.errorState)

onBeforeMount(() => store.fetchWikibasePage())
</script>

<template>
	<v-container class="wikibase-table-container my-0 px-6 py-8">
		<v-alert v-if="error" type="error" variant="tonal" title="Error">Error fetching data</v-alert>
		<wikibase-total-container />
		<v-container v-if="totalCount && showCount" class="show-count mb-6 pa-0">
			Showing {{ showCount.toLocaleString('en') }} of
			{{ totalCount.toLocaleString('en') }} instances
		</v-container>
		<wikibase-search />
		<WikibaseTable />
	</v-container>
</template>

<style lang="css">
.show-count {
	font-family: Roboto;
	font-size: 16px;
	color: #000;
}
</style>
