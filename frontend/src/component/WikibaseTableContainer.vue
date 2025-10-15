<script setup lang="ts">
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import WikibaseTypeFilter from '@/component/wikibase-table/WikibaseTypeFilter.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { onBeforeMount } from 'vue'

const store = useWikiStore()
onBeforeMount(() => store.fetchWikibasePage())
</script>

<template>
	<WikibaseTypeFilter />
	<WikibaseTable />
</template>

<style scoped></style>
