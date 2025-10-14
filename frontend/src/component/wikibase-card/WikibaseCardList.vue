<script setup lang="ts">
import WikibaseCard from '@/component/wikibase-card/WikibaseCard.vue'
import { useWikiStore } from '@/stores/wikibase-page-store'
import { computed } from 'vue'

const store = useWikiStore()

const wikibases = computed(() => store.wikibasePage.data?.wikibaseList.data)
</script>

<template>
	<v-container v-if="wikibases" class="wikibase-card-container ma-0 pa-0">
		<WikibaseCard v-for="(wikibase, index) in wikibases" :key="index" :wikibase="wikibase" />
	</v-container>
</template>

<style lang="css">
.wikibase-card-container {
	display: flex;
	flex-flow: row wrap;
	justify-content: space-evenly;
	align-items: stretch;
}
</style>
