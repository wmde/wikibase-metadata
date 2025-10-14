<script setup lang="ts">
defineProps<{ label: string; stat: number | undefined }>()
</script>

<template>
  <v-container class="stat-container pa-0">
    <v-label class="stat-label">{{ label }}</v-label>
    <div class="stat">
      <template v-if="stat != undefined">
        {{ stat.toLocaleString() }}
      </template>
    </div>
  </v-container>
</template>

<style lang="css"></style>
