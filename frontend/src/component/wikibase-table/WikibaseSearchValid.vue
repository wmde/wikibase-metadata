<script setup lang="ts">
import { useWikiPageStore } from '@/stores/wikibase-page-store'
import { computed } from 'vue'

const { menuValue, searchValue } = defineProps<{
	menuValue: 'instances' | 'items'
	searchValue: string
}>()

const store = useWikiPageStore()

const ALLOWED_CHARACTERS = /^[A-Za-z0-9\-_ .]*$/
type RuleResult = true | { prepend?: string; includeValue?: boolean; append?: string }
const displayRules = computed((): ((value: string) => RuleResult)[] => [
	(value: string) =>
		menuValue != 'instances' ||
		ALLOWED_CHARACTERS.test(value) || { prepend: 'Disallowed Characters' },
	(value: string) =>
		menuValue != 'instances' ||
		value.length == 0 ||
		store.wikibasePage.loading ||
		(store.wikibasePage.data && store.wikibasePage.data.meta.totalCount > 0) || {
			prepend: 'No results for ',
			includeValue: true,
			append: ' — try a different keyword or category'
		}
])
const displayRuleResults = computed(() =>
	displayRules.value.map((rule) => rule(searchValue)).filter((result) => result != true)
)
</script>

<template>
	<v-label class="search-error">
		<div v-for="(result, idx) in displayRuleResults" :key="idx">
			<span v-if="result.prepend" class="prepend">{{ result.prepend }}</span>
			<span v-if="result.includeValue" class="search-value">"{{ searchValue }}"</span>
			<span v-if="result.append" class="append">{{ result.append }}</span>
		</div>
	</v-label>
</template>

<style lang="scss">
.search-error {
	font-family: Roboto;
	font-size: 14px;
	color: rgb(107, 114, 128);
	margin-top: 8px;
	display: flex;
	flex-flow: column nowrap;
	align-items: start;
	span.search-value {
		color: black;
		font-weight: bolder;
	}
}
</style>
