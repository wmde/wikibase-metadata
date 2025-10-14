<script setup lang="ts">
import img from '@/media/icon/wikibase_symbol_RGB.png';
</script>

<template>
  <v-container class="pa-1 header">
    <v-container class="ma-0 pa-0 icon"><v-img :src="img" eager  /></v-container>
    <v-container class="ma-0 pa-0 title">Suite Scraper</v-container>
  </v-container>
</template>

<style lang="css">
.header {
  display: flex;
  flex-flow: row wrap;
  gap: 8px;
  width: 100%;
  align-items: center;
}
.icon {
  width: auto;
}
.icon .v-img {
  height: 50px;
  width: 50px;
}
.title {
  width: auto;
  flex-grow: 1;
}
</style>
