<script setup lang="ts">
import { WikibaseType } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import typeTitle from '@/util/type-title'
import { ref, watch } from 'vue'

const store = useWikiStore()

const includedTypes = ref<WikibaseType[]>(store.wikibaseFilter.wikibaseType?.include ?? [])
const typeOptions = [
	WikibaseType.Cloud,
	WikibaseType.Suite,
	WikibaseType.Other,
	WikibaseType.Test,
	WikibaseType.Unknown
].map((t) => ({ value: t, title: typeTitle(t) }))
watch(includedTypes, () => store.includeWikibaseTypes(includedTypes.value))
</script>

<template>
	<v-select
		class="wikibase-type-filter"
		label="Include Wikibase Types"
		v-model="includedTypes"
		:items="typeOptions"
		multiple
		chips
	/>
</template>
