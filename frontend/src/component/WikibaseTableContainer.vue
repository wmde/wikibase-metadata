<script setup lang="ts">
import WikibaseListStatus from '@/component/wikibase-table/WikibaseListStatus.vue'
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import WikibaseTypeFilter from '@/component/wikibase-table/WikibaseTypeFilter.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { onBeforeMount } from 'vue'

const store = useWikiStore()
onBeforeMount(() => store.fetchWikibasePage())
</script>

<template>
	<WikibaseListStatus />
	<WikibaseTypeFilter />
	<WikibaseTable />
</template>

<style scoped></style>
