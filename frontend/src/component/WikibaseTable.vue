<script setup lang="ts">
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
  <v-table v-if="wikibases" striped="even">
    <thead>
      <tr>
        <th>Id</th>
        <th>Type</th>
        <th>URL</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(wikibase, index) in wikibases" :key="index">
        <td>{{ wikibase.id }}</td>
        <td>{{ wikibase.wikibaseType }}</td>
        <td>{{ wikibase.urls.baseUrl }}</td>
      </tr>
    </tbody>
  </v-table>
</template>

<style lang="css">
.wikibase-card-container {
  display: flex;
  flex-flow: row wrap;
  gap: 6px;
  justify-content: space-evenly;
}
</style>
