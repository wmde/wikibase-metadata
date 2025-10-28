<script setup lang="ts">
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import WikibaseTypeFilter from '@/component/wikibase-table/WikibaseTypeFilter.vue'
import type { WbFragment } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed, onBeforeMount } from 'vue'

const store = useWikiStore()

const error = computed(() => store.wikibasePage.errorState)
const loading = computed(() => store.wikibasePage.loading)
const wikibases = computed<WbFragment[] | undefined>(
	() => store.wikibasePage.data?.wikibaseList.data
)

onBeforeMount(() => store.fetchWikibasePage())
</script>

<template>
	<v-container class="wikibase-table-container ma-0 pa-0">
		<WikibaseTypeFilter />
		<WikibaseTable :error="error" :loading="loading" :wikibases="wikibases" />
	</v-container>
</template>

<style scoped></style>
