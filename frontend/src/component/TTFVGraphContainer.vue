<script setup lang="ts">
import { useWikiTTFVStore } from '@/stores/wikibase-ttfv-store'
import { computed, onBeforeMount } from 'vue'

const store = useWikiTTFVStore()
const data = computed(() => store.wikibases.data)

onBeforeMount(() => store.fetchWikibases())
</script>

<template>
	<v-container class="ttfv-graph-container my-0 px-6 py-8">
		<v-container>{{ data }}</v-container>
	</v-container>
</template>

<style lang="scss"></style>
