<script setup lang="ts">
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import WikibaseTypeFilter from '@/component/wikibase-table/WikibaseTypeFilter.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { onBeforeMount } from 'vue'

const store = useWikiStore()
onBeforeMount(() => store.fetchWikibasePage())
</script>

<template>
	<v-container class="wikibase-table-container ma-0 pa-0">
		<WikibaseTypeFilter />
		<WikibaseTable />
	</v-container>
</template>

<style scoped></style>
