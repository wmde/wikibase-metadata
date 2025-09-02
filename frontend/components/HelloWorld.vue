<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ msg: string }>()

const count = ref(0)
</script>

<template>
  <h1 class="text-3xl font-semibold">{{ msg }}</h1>

  <div class="card">
    <button
      type="button"
      class="rounded-md bg-indigo-600 px-4 py-2 text-white shadow hover:bg-indigo-500"
      @click="count++"
    >
      count is {{ count }}
    </button>
    <p class="mt-4 text-sm text-gray-600 dark:text-gray-300">
      Edit <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>

  <p class="mt-6">
    Check out
    <a class="underline" href="https://vuejs.org/guide/quick-start.html#local" target="_blank">create-vue</a>,
    the official Vue + Vite starter
  </p>
  <p class="text-sm text-gray-600 dark:text-gray-300">
    Learn more about IDE Support for Vue in the
    <a
      class="underline"
      href="https://vuejs.org/guide/scaling-up/tooling.html#ide-support"
      target="_blank"
    >Vue Docs Scaling up Guide</a>.
  </p>
  <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
