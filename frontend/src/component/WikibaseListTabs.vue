<script setup lang="ts">
import WikibaseCardList from '@/component/WikibaseCardList.vue'
import WikibaseTable from '@/component/WikibaseTable.vue'
import { useWikiStore } from '@/stores/wikibase-page'
import { onBeforeMount, ref } from 'vue'

const store = useWikiStore()
onBeforeMount(() => store.fetchWikibasePage())

const tab = ref('table')
</script>

<template>
  <v-tabs v-model="tab">
    <v-tab value="card">Cards</v-tab>
    <v-tab value="table">Table</v-tab>
  </v-tabs>
  <v-tabs-window v-model="tab">
    <v-tabs-window-item value="card">
      <WikibaseCardList />
    </v-tabs-window-item>
    <v-tabs-window-item value="table">
      <WikibaseTable />
    </v-tabs-window-item>
  </v-tabs-window>
</template>

<style scoped></style>
