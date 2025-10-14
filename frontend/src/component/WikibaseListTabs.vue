<script setup lang="ts">
import WikibaseCardList from '@/component/wikibase-card/WikibaseCardList.vue'
import WikibaseListStatus from '@/component/WikibaseListStatus.vue'
import WikibaseTable from '@/component/WikibaseTable.vue'
import WikibaseTypeFilter from '@/component/WikibaseTypeFilter.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { onBeforeMount, ref } from 'vue'

const store = useWikiStore()
onBeforeMount(() => store.fetchWikibasePage())

const tab = ref<'table' | 'card'>('table')
</script>

<template>
	<v-tabs v-model="tab">
		<v-tab value="card">Cards</v-tab>
		<v-tab value="table">Table</v-tab>
	</v-tabs>
	<WikibaseListStatus />
	<WikibaseTypeFilter />
	<v-tabs-window v-model="tab">
		<v-tabs-window-item value="card">
			<WikibaseCardList />
		</v-tabs-window-item>
		<v-tabs-window-item value="table">
			<WikibaseTable />
		</v-tabs-window-item>
	</v-tabs-window>
</template>

<style scoped></style>
