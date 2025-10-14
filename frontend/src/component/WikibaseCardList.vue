<script setup lang="ts">
import WikibaseCard from '@/component/WikibaseCard.vue'
import { useWikiStore } from '@/stores/wikibase-page'
import { computed, onBeforeMount } from 'vue'

const store = useWikiStore()
onBeforeMount(() => store.fetchWikibasePage())

const error = computed(() => store.wikibasePage.errorState)
const loading = computed(() => store.wikibasePage.loading)
const count = computed(() => store.wikibasePage.data?.wikibaseList.meta.totalCount)
const wikibases = computed(() => store.wikibasePage.data?.wikibaseList.data)
</script>

<template>
  <p v-if="error">Error</p>
  <p v-if="loading">Loading</p>
  <p>Count: {{ count }}</p>
  <div v-if="wikibases" class="wikibase-card-container">
    <WikibaseCard v-for="(wikibase, index) in wikibases" :key="index" :wikibase="wikibase" />
  </div>
</template>

<style lang="css" scoped></style>
