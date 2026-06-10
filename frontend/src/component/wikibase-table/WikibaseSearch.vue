<script setup lang="ts">
import { useWikiStore } from '@/stores/wikibase-page-store'
import { debounce } from '@/util/debounce'
import { mdiMagnify } from '@mdi/js'
import { computed, ref, watch } from 'vue'

const store = useWikiStore()

const searchValue = ref('')
const [deouncedSearch] = debounce((v: string) => store.searchWikibaseText(v), 300)
watch(searchValue, () => deouncedSearch(searchValue.value))

const rules: ((value: string) => true | string)[] = [
	(value: string) => /^[a-z0-9\- .]*$/.test(value) || 'Disallowed Characters'
]
type RuleResult = true | { prepend?: string; includeValue?: boolean; append?: string }
const displayRules = computed((): ((value: string) => RuleResult)[] => [
	(value: string) => /^[a-z0-9\- .]*$/.test(value) || { prepend: 'Disallowed Characters' },
	(value: string) =>
		value.length == 0 || (store.wikibasePage.data && store.wikibasePage.data.meta.totalCount > 0)
			? true
			: {
					prepend: 'No results for ',
					includeValue: true,
					append: ' — try a different keyword or category'
				}
])
const displayRuleResults = computed(() =>
	displayRules.value.map((rule) => rule(searchValue.value)).filter((result) => result != true)
)

const focused = ref(false)
</script>

<template>
	<v-container class="search-container ma-0 mb-6 pa-0">
		<v-container :class="`ma-0 pa-0 pl-3 search-text ${focused ? 'search-text-focused' : ''}`">
			<v-text-field
				class="ma-0 pa-0"
				variant="plain"
				:prepend-icon="mdiMagnify"
				v-model="searchValue"
				label="Search Wikibase instances..."
				:rules="rules"
				:focused="focused"
				@update:focused="(v: boolean) => (focused = v)"
			/>
		</v-container>
		<v-label class="search-error">
			<div v-for="(result, idx) in displayRuleResults" :key="idx">
				<span v-if="result.prepend" class="prepend">{{ result.prepend }}</span>
				<span v-if="result.includeValue" class="search-value">"{{ searchValue }}"</span>
				<span v-if="result.append" class="append">{{ result.append }}</span>
			</div>
		</v-label>
	</v-container>
</template>

<style lang="scss">
.search-text {
	border: 1px solid oklch(87.2% 0.01 285.338);
	border-radius: calc(0.625rem - 2px);
	background: white;
	font-family: Roboto;

	div.v-input__details {
		display: none;
	}

	div.v-input__prepend {
		padding-top: 14px !important;
	}
	label.v-label {
		top: 14px !important;
		transform: none !important;
	}
	label.v-field-label--floating {
		display: none;
	}

	input {
		margin: 0 0 4px;
		padding: 0;
		font-size: 16px;
		color: rgb(0, 0, 0);
	}
	label.v-field-label--floating {
		color: #444;
	}
}
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

.search-text-focused {
	border-color: rgb(54, 40, 245);
}
</style>
