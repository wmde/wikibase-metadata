<script setup lang="ts">
import { type WbItemFragment } from '@/graphql/types'
import { useWikiListStore } from '@/stores/wikibase-list-store'
import { computed, onBeforeMount } from 'vue'

const store = useWikiListStore()

const loading = computed(() => store.wikibaseList.loading)
const wikibases = computed<WbItemFragment[] | undefined>(() =>
	store.wikibaseList.loading ? undefined : store.wikibaseList.data?.data
)

onBeforeMount(() => store.fetchWikibaseList())
</script>

<template>
	<template v-if="loading">Loading</template>
	<template v-if="wikibases?.length">
		<div>
			<wikibase-item v-for="wiki in wikibases" :key="wiki.id" :wiki="wiki" />
		</div>
	</template>
</template>

<style lang="css"></style>
