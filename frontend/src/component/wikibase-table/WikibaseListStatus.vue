<script setup lang="ts">
import LocaleNumber from '@/component/LocaleNumber.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed } from 'vue'

const store = useWikiStore()

const error = computed(() => store.wikibasePage.errorState)
const loading = computed(() => store.wikibasePage.loading)
const count = computed(() => store.wikibasePage.data?.wikibaseList.meta.totalCount)
</script>

<template>
	<v-container>
		<p v-if="error">Error</p>
		<p v-if="loading">Loading</p>
		<p>Count: <LocaleNumber :stat="count" /></p>
	</v-container>
</template>

<style lang="css"></style>
