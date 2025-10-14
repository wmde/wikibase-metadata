<script setup lang="ts">
defineProps<{ stat: number | undefined }>()
</script>

<template>
  <template v-if="stat != undefined">{{ stat.toLocaleString() }}</template>
</template>

<style lang="css"></style>
