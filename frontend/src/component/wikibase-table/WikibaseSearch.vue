<script setup lang="ts">
import { useWikiStore } from '@/stores/wikibase-page-store'
import { debounce } from '@/util/debounce'
import { ref, watch } from 'vue'

const store = useWikiStore()

const searchValue = ref('')
const [deouncedSetValue] = debounce((v: string) => store.searchWikibaseText(v), 300)
watch(searchValue, () => deouncedSetValue(searchValue.value))
</script>

<template>
	<v-container class="search-text">
		<v-text-field v-model="searchValue" label="Search Wikibases" />
		<v-container>{{ searchValue }}</v-container>
		<v-container>{{ store.wikibaseFilter.searchText }}</v-container>
	</v-container>
</template>

<style lang="css"></style>
