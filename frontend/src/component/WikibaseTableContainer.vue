<script setup lang="ts">
import WikibaseItemList from '@/component/wikibase-item-list/WikibaseItemList.vue'
import WikibaseSearch from '@/component/wikibase-table/WikibaseSearch.vue'
import WikibaseTable from '@/component/wikibase-table/WikibaseTable.vue'
import WikibaseTotalContainer from '@/component/wikibase-table/WikibaseTotalContainer.vue'
import { useWikiPageStore } from '@/stores/wikibase-page-store'
import { debounce } from '@/util/debounce'
import { computed, onBeforeMount, ref, watch } from 'vue'

const store = useWikiPageStore()
const showCount = computed(() => store.wikibasePage.data?.data.length)
const totalCount = computed(() => store.wikibasePage.data?.meta.totalCount)

const error = computed(() => store.wikibasePage.errorState)

const menuValue = ref<'instances' | 'items'>('instances')
const setMenuValue = (v: 'instances' | 'items') => (menuValue.value = v)

const searchValue = ref('')
const setSearchValue = (s: string) => (searchValue.value = s)
const [debouncedSearchInstances] = debounce(
	(v: string | undefined) => store.searchWikibaseText(v),
	300
)
const debouncedSearchValue = ref(searchValue.value)
const [setDebouncedSearchValue] = debounce((s: string) => (debouncedSearchValue.value = s), 1000)
watch(searchValue, () => {
	if (menuValue.value == 'instances') {
		debouncedSearchInstances(searchValue.value ? searchValue.value : undefined)
	}
	if (menuValue.value == 'items') {
		setDebouncedSearchValue(searchValue.value)
	}
})

onBeforeMount(() => store.fetchWikibasePage())
</script>

<template>
	<v-container class="wikibase-table-container my-0 px-6 py-8">
		<v-alert v-if="error" type="error" variant="tonal" title="Error">Error fetching data</v-alert>
		<wikibase-total-container />
		<wikibase-search
			:menu-value="menuValue"
			:set-menu-value="setMenuValue"
			:set-search-value="setSearchValue"
		/>
		<template v-if="menuValue == 'instances'">
			<v-container v-if="totalCount && showCount" class="show-count mb-6 pa-0">
				Showing {{ showCount.toLocaleString('en') }} of
				{{ totalCount.toLocaleString('en') }} instances
			</v-container>
			<wikibase-table />
		</template>
		<template v-if="menuValue == 'items'">
			<wikibase-item-list :search-value="debouncedSearchValue" />
		</template>
	</v-container>
</template>

<style lang="css">
.show-count {
	font-family: Roboto;
	font-size: 16px;
	color: #000;
}
</style>
