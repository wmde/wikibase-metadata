<script setup lang="ts">
import LocaleNumber from '@/component/LocaleNumber.vue'
import WikibaseCard from '@/component/wikibase-card/WikibaseCard.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed } from 'vue'

const store = useWikiStore()

const error = computed(() => store.wikibasePage.errorState)
const loading = computed(() => store.wikibasePage.loading)
const count = computed(() => store.wikibasePage.data?.wikibaseList.meta.totalCount)
const wikibases = computed(() => store.wikibasePage.data?.wikibaseList.data)
</script>

<template>
	<p v-if="error">Error</p>
	<p v-if="loading">Loading</p>
	<p>Count: <LocaleNumber :stat="count" /></p>
	<div v-if="wikibases" class="wikibase-card-container">
		<WikibaseCard v-for="(wikibase, index) in wikibases" :key="index" :wikibase="wikibase" />
	</div>
</template>

<style lang="css">
.wikibase-card-container {
	display: flex;
	flex-flow: row wrap;
	justify-content: space-evenly;
	align-items: stretch;
}
</style>
