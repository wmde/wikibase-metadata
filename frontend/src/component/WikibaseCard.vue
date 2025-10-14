<script setup lang="ts">
import type { WbFragment } from '@/graphql/types'

defineProps<{ wikibase: WbFragment }>()
</script>

<template>
  <v-card variant="outlined" class="wikibase-card">
    <p>Id: {{ wikibase.id }}</p>
    <p>Type: {{ wikibase.wikibaseType }}</p>
    <p>URL: {{ wikibase.urls.baseUrl }}</p>
  </v-card>
</template>

<style lang="css" scoped></style>
