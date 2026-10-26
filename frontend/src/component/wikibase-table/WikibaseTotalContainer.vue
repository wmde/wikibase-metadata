<script setup lang="ts">
import WikibaseTotalBox from '@/component/wikibase-table/WikibaseTotalBox.vue'
import { useWikiTotalStore } from '@/stores/wikibase-total-store'
import { computed, onBeforeMount } from 'vue'

const totalStore = useWikiTotalStore()
const totalCount = computed(() => totalStore.wikibaseTotal.data?.totalCount)
const totalEdits = computed(() => totalStore.wikibaseTotal.data?.totalEdits)
const totalTriples = computed(() => totalStore.wikibaseTotal.data?.totalTriples)

onBeforeMount(() => totalStore.fetchWikibaseTotal())
</script>

<template>
	<v-container class="wikibase-total-container pa-0 ma-0 mb-8">
		<wikibase-total-box
			v-if="totalCount"
			:value="totalCount"
			label="Instances (curated from 1,500+ Wikibases)"
		/>
		<wikibase-total-box v-if="totalTriples" :value="totalTriples" label="Total Triples" />
		<wikibase-total-box v-if="totalEdits" :value="totalEdits" label="Edits (30 days)" />
	</v-container>
</template>

<style lang="css">
.wikibase-total-container {
	display: flex;
	flex-flow: row wrap;
	gap: 1rem;
}
</style>
