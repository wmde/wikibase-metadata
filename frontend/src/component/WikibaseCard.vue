<script setup lang="ts">
import type { WbFragment } from '@/graphql/types'

defineProps<{ wikibase: WbFragment }>()
</script>

<template>
  <div class="wikibase-card">
    <p>Id: {{ wikibase.id }}</p>
    <p>Type: {{ wikibase.wikibaseType }}</p>
    <p>URL: {{ wikibase.urls.baseUrl }}</p>
  </div>
</template>

<style lang="css" scoped></style>
