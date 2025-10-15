<script setup lang="ts">
import { WikibaseType } from '@/graphql/types'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { ref, watch } from 'vue'

const store = useWikiStore()

const excludedTypes = ref<WikibaseType[]>(store.wikibaseFilter.wikibaseType?.exclude ?? [])
const typeOptions = [WikibaseType.Cloud, WikibaseType.Suite, WikibaseType.Other, WikibaseType.Test]
watch(excludedTypes, () => store.excludeWikibaseTypes(excludedTypes.value))
</script>

<template>
	<v-container>
		<v-select
			label="Exclude Wikibase Types"
			v-model="excludedTypes"
			:items="typeOptions"
			multiple
			chips
		/>
	</v-container>
</template>

<style lang="css"></style>
