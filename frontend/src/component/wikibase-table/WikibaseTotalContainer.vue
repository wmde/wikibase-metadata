<script setup lang="ts">
import WikibaseTotalBox from '@/component/wikibase-table/WikibaseTotalBox.vue'
import { useMenuStore } from '@/stores/menu-store'
import { useWikiListStore } from '@/stores/wikibase-list-store'
import { useWikiPageStore } from '@/stores/wikibase-page-store'
import { computed } from 'vue'

const menuStore = useMenuStore()
const menuValue = computed(() => menuStore.value)

const listStore = useWikiListStore()
const listCount = computed(() => listStore.wikibaseList.data?.meta.totalCount)

const pageStore = useWikiPageStore()
const totalCount = computed(() => pageStore.wikibasePage.data?.meta.totalCount)
const totalEdits = computed(() => pageStore.wikibasePage.data?.meta.totalEdits)
const totalTriples = computed(() => pageStore.wikibasePage.data?.meta.totalTriples)
</script>

<template>
	<v-container class="wikibase-total-container pa-0 ma-0 mb-8">
		<template v-if="menuValue == 'instances'">
			<wikibase-total-box v-if="totalCount" :value="totalCount" label="Total Instances" />
		</template>
		<template v-else>
			<wikibase-total-box
				v-if="listCount"
				:value="listCount"
				label="Instances (curated from 1,500+ Wikibases)"
			/>
		</template>
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
