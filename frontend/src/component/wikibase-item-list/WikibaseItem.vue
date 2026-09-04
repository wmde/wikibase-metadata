<script setup lang="ts">
import { type WbItemFragment } from '@/graphql/types'
import getActionApiUrl from '@/util/getActionApiUrl'
import { computed, onMounted, ref } from 'vue'

const { searchValue, wiki } = defineProps<{ searchValue: string; wiki: WbItemFragment }>()

const actionApiUrl = computed(() => getActionApiUrl(wiki.urls.baseUrl, wiki.urls.scriptPath))

const data = ref()
const loading = ref(false)
const getData = async () => {
	if (actionApiUrl.value && searchValue) {
		loading.value = true
		const response = await fetch(
			`${actionApiUrl.value}?action=wbsearchentities&search=${searchValue}&language=en&format=json`
		)
		data.value = await response.json()
		loading.value = false
	}
}

onMounted(getData)
</script>

<template>
	<div class="wikibase-item">
		<h4>({{ wiki.id }}) {{ wiki.title }}</h4>
		<p>
			<a :href="getActionApiUrl(wiki.urls.baseUrl, wiki.urls.scriptPath) ?? undefined">
				Action API
			</a>
		</p>
		<p>Searching: {{ searchValue }}</p>
		<p>Loading: {{ loading }}</p>
		<p>Result: {{ data }}</p>
	</div>
</template>

<style lang="css"></style>
