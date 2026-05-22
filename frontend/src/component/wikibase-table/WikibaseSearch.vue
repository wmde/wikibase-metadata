<script setup lang="ts">
import { useWikiStore } from '@/stores/wikibase-page-store'
import { debounce } from '@/util/debounce'
import { mdiMagnify } from '@mdi/js'
import { ref, watch } from 'vue'

const store = useWikiStore()

const searchValue = ref('')
const [deouncedSetValue] = debounce((v: string) => store.searchWikibaseText(v), 300)
watch(searchValue, () => deouncedSetValue(searchValue.value))
</script>

<template>
	<v-container class="search-text ma-0 mb-6 pa-0 pl-3">
		<v-text-field
			class="ma-0 pa-0"
			variant="plain"
			:prepend-icon="mdiMagnify"
			v-model="searchValue"
			label="Search Wikibase instances..."
		/>
	</v-container>
</template>

<style lang="scss">
.search-text {
	border: 1px solid oklch(87.2% 0.01 285.338);
	border-radius: calc(0.625rem - 2px);
	background: #f3f3f5;
	font-family: Roboto;

	.v-input__details {
		display: none;
	}
	div.v-input__prepend {
		padding-top: 14px !important;
	}
	label.v-label {
		top: 14px !important;
	}
	input {
		margin: 0 0 4px;
		padding: 0;
		// font-family: Roboto;
		font-size: 16px;
		color: rgb(0, 0, 0);
	}
	label.v-field-label--floating {
		color: #444;
	}
}
</style>
