<script setup lang="ts">
import WikibaseDetailCard from '@/component/wikibase-table/wikibase-detail-card/WikibaseDetailCard.vue'
import { useSingleWikiStore } from '@/stores/wikibase-store'
import { computed, ref, watch } from 'vue'

const props = defineProps<{ wikibaseId: number }>()

const store = useSingleWikiStore()
const wikibase = computed(() => store.wikibase.data?.wikibase)
const loading = computed(() => store.wikibase.loading)

const dialog = ref(false)
watch(dialog, () => dialog.value && store.searchWikibase(props.wikibaseId))
</script>

<template>
	<v-dialog class="wikibase-detail-dialog" width="auto" v-model="dialog">
		<template v-slot:activator="{ props: activatorProps }">
			<v-btn v-bind="activatorProps" density="comfortable" variant="outlined" class="detail-button">
				Details
			</v-btn>
		</template>
		<WikibaseDetailCard :wikibase="wikibase" :loading="loading" />
	</v-dialog>
</template>

<style lang="css">
.detail-button {
	background-color: oklch(96.7% 0.003 264.542);
	text-transform: none;
	font-family: Roboto;
	font-size: 16px;
	letter-spacing: inherit;
	border-radius: calc(0.625rem - 2px);
	border-color: rgba(0, 0, 0, 0.1);
}
.detail-button :hover {
	background-color: oklch(92.8% 0.006 264.531);
}
</style>
