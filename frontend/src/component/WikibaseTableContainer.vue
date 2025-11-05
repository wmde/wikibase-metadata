<script setup lang="ts">
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import WikibaseTypeFilter from '@/component/wikibase-table/WikibaseTypeFilter.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed, onBeforeMount } from 'vue'

const store = useWikiStore()

const error = computed(() => store.wikibasePage.errorState)

onBeforeMount(() => store.fetchWikibasePage())
</script>

<template>
	<v-container class="wikibase-table-container ma-0 pa-0">
		<WikibaseTypeFilter />
		<v-alert v-if="error" type="error" variant="tonal" title="Error">Error fetching data</v-alert>
		<WikibaseTable />
	</v-container>
</template>
