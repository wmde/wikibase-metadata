<script setup lang="ts">
import { useSingleWikiStore } from '@/stores/wikibase-store'
import { computed, ref, watch } from 'vue'
import WikibaseDetailCard from './WikibaseDetailCard.vue'

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
			<v-btn v-bind="activatorProps">VIEW</v-btn>
		</template>
		<WikibaseDetailCard :wikibase="wikibase" :loading="loading" />
	</v-dialog>
</template>
