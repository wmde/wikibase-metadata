<script setup lang="ts">
import WikibaseTypeFilter from '@/component/wikibase-table/WikibaseTypeFilter.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { onBeforeMount } from 'vue'
import WikibaseServerTable from './wikibase-table/WikibaseServerTable.vue'

const store = useWikiStore()

onBeforeMount(() => store.fetchWikibasePage())
</script>

<template>
	<v-container class="wikibase-table-container ma-0 pa-0">
		<WikibaseTypeFilter />

		<WikibaseServerTable />
	</v-container>
</template>

<style scoped></style>
