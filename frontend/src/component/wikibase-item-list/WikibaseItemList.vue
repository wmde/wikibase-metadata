<script setup lang="ts">
import WikibaseItem from '@/component/wikibase-item-list/WikibaseItem.vue'
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
		<div class="wikibase-item-list-container">
			<wikibase-item v-for="wiki in wikibases" :key="wiki.id" :wiki="wiki" />
		</div>
	</template>
</template>

<style lang="scss">
.wikibase-item-list-container {
	.wikibase-item {
		margin: 8px auto;
	}
}
</style>
