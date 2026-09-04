<script setup lang="ts">
import type { WbItemFragment } from '@/graphql/types'
import getActionApiUrl from '@/util/getActionApiUrl'
import { computed, ref, watch } from 'vue'

const { searchValue, wiki } = defineProps<{ searchValue: string; wiki: WbItemFragment }>()

const actionApiUrl = computed(() => getActionApiUrl(wiki.urls.baseUrl, wiki.urls.scriptPath))

const data = ref()
const loading = ref(false)
const getData = async () => {
	if (actionApiUrl.value && searchValue) {
		const request = new Request(
			`${actionApiUrl.value}?action=wbsearchentities&search=${searchValue}&language=en&format=json`,
			{ headers: [] }
		)
		loading.value = true
		const response = await fetch(request)
		data.value = await response.json()
		loading.value = false
	}
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
