<script setup lang="ts">
import type { WbItemFragment } from '@/graphql/types'
import getActionApiUrl from '@/util/getActionApiUrl'
import { computed, ref, watch } from 'vue'

const { searchValue, wiki } = defineProps<{ searchValue: string; wiki: WbItemFragment }>()

const actionApiUrl = computed(() => getActionApiUrl(wiki.urls.baseUrl, wiki.urls.scriptPath))

const data = ref<SearchResult>()
const status = ref<{ code: number; text: string }>()
const loading = ref(false)
const getData = async () => {
	if (actionApiUrl.value && searchValue) {
		const request = new Request(
			`${actionApiUrl.value}?action=wbsearchentities&search=${searchValue}&language=en&format=json`,
			{ headers: [] }
		)
		loading.value = true
		const response = await fetch(request)
		status.value = { code: response.status, text: response.statusText }
		if (status.value.code == 200) {
			data.value = (await response.json()) as SearchResult
		}
		loading.value = false
	}
}

type SearchResult = {
	searchInfo: {
		search: string
	}
	search: {
		id: string
		title: string
		pageid: number
		repository: string
		url: string
		concepturi: string
		label: string
		description: string
		match: {
			type: string
			language: string
			text: string
		}
	}[]
	success: number
}

// You cannot directly watch the prop for changes
// But you can watch, essentially, a reference to the value of the prop
const searchValueRef = computed(() => searchValue)
watch(searchValueRef, getData)
</script>

<template>
	<div class="wikibase-item">
		<h4>({{ wiki.id }}) {{ wiki.title }}</h4>
		<p>
			<a :href="actionApiUrl ?? undefined">Action API</a>
		</p>
		<p>Searching: {{ searchValue }}</p>
		<p>Loading: {{ loading }}</p>
		<p>Result: {{ data }}</p>
	</div>
</template>

<style lang="css"></style>
