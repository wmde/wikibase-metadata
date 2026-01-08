<script setup lang="ts">
import WikibaseDetailCard from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCard.vue'
import { router } from '@/router'
import { useSingleWikiStore } from '@/stores/wikibase-store'
import { computed, onBeforeMount } from 'vue'

const store = useSingleWikiStore()

const loading = computed(() => store.wikibase.loading)
const wikibaseId = computed(() =>
	router.currentRoute.value.params['id']
		? Number.parseInt(router.currentRoute.value.params['id'] as string)
		: undefined
)
const wikibase = computed(() => store.wikibase.data?.wikibase)

onBeforeMount(() => wikibaseId.value && store.searchWikibase(wikibaseId.value))
</script>

<template>
	<v-container class="ma-0 pa-0">
		<WikibaseDetailCard :loading="loading" :wikibase="wikibase" />
	</v-container>
</template>
