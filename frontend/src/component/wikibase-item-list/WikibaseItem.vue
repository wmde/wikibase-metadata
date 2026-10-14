<script setup lang="ts">
import type { WbItemFragment } from '@/graphql/types'
import DataFetcher from '@/util/fetch-data'
import getActionApiUrl from '@/util/getActionApiUrl'
import { computed, watch } from 'vue'

const { searchValue, wiki } = defineProps<{ searchValue: string; wiki: WbItemFragment }>()

const fetcher = new DataFetcher(getActionApiUrl(wiki.urls.baseUrl, wiki.urls.scriptPath))

const actionApiUrl = computed(() => fetcher.actionApiUrl)
const data = computed(() => fetcher.data)
const status = computed(() => fetcher.status)
const loading = computed(() => fetcher.loading)

// You cannot directly watch the prop for changes
// But you can watch, essentially, a reference to the value of the prop
const searchValueRef = computed(() => searchValue)
watch(searchValueRef, () => fetcher.getData(searchValueRef.value))
</script>

<template>
	<div class="wikibase-item">
		<h4>({{ wiki.id }}) {{ wiki.title }}</h4>
		<p>
			<a :href="actionApiUrl ?? undefined">Action API</a>
		</p>
		<p>Searching: {{ searchValue }}</p>
		<p>Loading: {{ loading }}</p>
		<p>Status: {{ status }}</p>
		<p>Result: {{ data }}</p>
	</div>
</template>

<style lang="css"></style>
