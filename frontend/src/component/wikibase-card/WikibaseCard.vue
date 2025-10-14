<script setup lang="ts">
import type { WbFragment } from '@/graphql/types'
import { computed } from 'vue'
import WikibaseCardStatBlock from './WikibaseCardStatBlock.vue'

const props = defineProps<{ wikibase: WbFragment }>()
const editCount = computed(() =>
  props.wikibase.recentChangesObservations.mostRecent?.botChangeCount != undefined ||
  props.wikibase.recentChangesObservations.mostRecent?.humanChangeCount != undefined
    ? (props.wikibase.recentChangesObservations.mostRecent.botChangeCount ?? 0) +
      (props.wikibase.recentChangesObservations.mostRecent.humanChangeCount ?? 0)
    : undefined
)
</script>

<template>
  <v-card variant="outlined" class="wikibase-card pa-1">
    <v-container class="card-header pa-0">
      <v-container class="pa-0">
        <v-container class="pa-0 wikibase-url">{{ wikibase.urls.baseUrl }}</v-container>
        <div v-if="wikibase.description" class="description">{{ wikibase.description }}</div>
      </v-container>
      <v-container class="pa-0 wikibase-type">{{ wikibase.wikibaseType }}</v-container>
    </v-container>
    <v-container class="stat-block-container pa-0">
      <WikibaseCardStatBlock label="EDITS (30 DAYS)" :stat="editCount" />
      <WikibaseCardStatBlock
        label="TRIPLES"
        :stat="wikibase.quantityObservations.mostRecent?.totalTriples"
      />
    </v-container>
  </v-card>
</template>

<style lang="css">
.wikibase-card {
  display: flex;
  flex-flow: column nowrap;
  justify-content: space-between;
}
.card-header {
  display: flex;
  flex-flow: row nowrap;
  gap: 12px;
}
.wikibase-type {
  width: auto;
  align-self: stretch;
  align-content: center;
  font-weight: 500;
}
.stat-block-container {
  display: flex;
  flex-flow: row nowrap;
}
</style>
