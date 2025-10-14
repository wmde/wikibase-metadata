<script setup lang="ts">
defineProps<{ stat: number | undefined }>()
</script>

<template>
  <template v-if="stat != undefined">{{ stat.toLocaleString() }}</template>
  <template v-else>&#151;</template>
</template>

<style lang="css"></style>
