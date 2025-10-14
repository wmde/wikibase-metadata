<script setup lang="ts">
import { computed, onBeforeMount } from 'vue'
import { useWikiStore } from './stores/wikibase-page'

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
  <div v-if="wikibases">
    <div v-for="(wikibase, index) in wikibases" :key="index" class="wikibase-card">
      <p>Id: {{ wikibase.id }}</p>
      <p>Type: {{ wikibase.wikibaseType }}</p>
      <p>URL: {{ wikibase.urls.baseUrl }}</p>
    </div>
  </div>
</template>

<style scoped></style>
