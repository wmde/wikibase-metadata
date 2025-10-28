<script setup lang="ts">
import WikibaseTypeChip from '@/component/wikibase-table/WikibaseTypeChip.vue'
import { WikibaseType } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import uniqueValues from '@/util/uniqueValues'
import { computed, ref, watch } from 'vue'

const store = useWikiStore()

const showingTypes = computed(() =>
	store.wikibasePage.data
		? uniqueValues(
				store.wikibasePage.data.wikibaseList.data.map((w) => w.wikibaseType),
				(t) => t ?? 'UNKNOWN'
			)
		: []
)
const excludedTypes = ref<WikibaseType[]>(store.wikibaseFilter.wikibaseType?.exclude ?? [])
const typeOptions = [WikibaseType.Cloud, WikibaseType.Suite, WikibaseType.Other, WikibaseType.Test]
watch(excludedTypes, () => store.excludeWikibaseTypes(excludedTypes.value))
</script>

<template>
	<v-container class="wikibase-type-showing-list" v-if="showingTypes.length > 0">
		<v-label>Showing Wikibase Types:</v-label>
		<v-container class="pa-0 ma-0">
			<WikibaseTypeChip v-for="(t, index) in showingTypes" :key="index" :wikibase-type="t" />
		</v-container>
	</v-container>
	<v-select
		class="wikibase-type-filter"
		label="Exclude Wikibase Types"
		v-model="excludedTypes"
		:items="typeOptions"
		multiple
		chips
	/>
</template>

<style lang="css"></style>
