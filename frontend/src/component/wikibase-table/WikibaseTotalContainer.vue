<script setup lang="ts">
import WikibaseTotalBox from '@/component/wikibase-table/WikibaseTotalBox.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed } from 'vue'

const store = useWikiStore()
const totalCount = computed(() => store.wikibasePage.data?.meta.totalCount)
const totalEdits = computed(() => store.wikibasePage.data?.meta.totalEdits)
const totalTriples = computed(() => store.wikibasePage.data?.meta.totalTriples)
</script>

<template>
	<v-container class="wikibase-total-container pa-0 ma-0 mb-8">
		<wikibase-total-box v-if="totalCount" :value="totalCount" label="Total Instances" />
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
