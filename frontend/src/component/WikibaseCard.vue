<script setup lang="ts">
import type { WbFragment } from '@/graphql/types'

defineProps<{ wikibase: WbFragment }>()
</script>

<template>
  <v-card variant="outlined" class="wikibase-card pa-1">
    <v-container class="card-header pa-0">
      <v-container class="pa-0 wikibase-url">{{ wikibase.urls.baseUrl }}</v-container>
      <v-container class="pa-0 wikibase-type">{{ wikibase.wikibaseType }}</v-container>
    </v-container>
    <div v-if="wikibase.description" class="description">{{ wikibase.description }}</div>
    <v-container class="stat-container pa-0">
      <v-container class="edit-container pa-0">
        <v-label class="edit-label">EDITS (30 DAYS)</v-label>
        <div class="statistic edit-stat">
          <template
            v-if="
              wikibase.recentChangesObservations.mostRecent?.botChangeCount != undefined ||
              wikibase.recentChangesObservations.mostRecent?.humanChangeCount != undefined
            "
          >
            {{
              (wikibase.recentChangesObservations.mostRecent.botChangeCount ?? 0) +
              (wikibase.recentChangesObservations.mostRecent.humanChangeCount ?? 0)
            }}
          </template>
        </div>
      </v-container>
      <v-container class="triples-container pa-0">
        <v-label class="triples-label">TRIPLES</v-label>
        <div class="statistic triples-stat">
          {{ wikibase.quantityObservations.mostRecent?.totalTriples }}
        </div>
      </v-container>
    </v-container>
  </v-card>
</template>

<style lang="css">
.card-header {
  display: flex;
  flex-flow: row nowrap;
  justify-content: space-between;
}
.wikibase-type {
  width: auto;
}
.stat-container {
  display: flex;
  flex-flow: row nowrap;
}
</style>
