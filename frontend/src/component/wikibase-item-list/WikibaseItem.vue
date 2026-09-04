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
		<div class="header-container">
			<div class="wiki-title">{{ wiki.title }}</div>
			<div class="status">
				<template v-if="loading">Loading</template>
				<template v-else-if="status">
					<template v-if="status.code == 200">
						<div v-if="!data?.search.length" class="no-results">No Results</div>
					</template>
					<template v-else>
						<div class="error">{{ status.code }}: {{ status.text }}</div>
					</template>
				</template>
			</div>
		</div>
		<div v-if="data && data.search.length > 0" class="results-container">
			<div v-for="datum in data.search" :key="datum.id" class="result">
				<div class="item-label-container">
					<div class="item-label">
						<a :href="datum.url">{{ datum.label }}</a>
					</div>
					<div class="item-id">{{ datum.id }}</div>
				</div>
				<div class="description">{{ datum.description }}</div>
			</div>
		</div>
	</div>
</template>

<style lang="scss"></style>
