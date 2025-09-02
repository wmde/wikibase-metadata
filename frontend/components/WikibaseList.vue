<script setup lang="ts">
import { onMounted, ref } from 'vue'

type Wikibase = {
  id: string | number
  urls: { baseUrl: string }
}

const loading = ref(true)
const error = ref<string | null>(null)
const items = ref<Wikibase[]>([])

const endpoint = import.meta.env.DEV
  ? 'http://localhost:8000/graphql'
  : '/graphql'

const query = `query q {\n  wikibaseList(pageNumber: 1, pageSize: 1000000) {\n    data {\n      id\n      urls {\n        baseUrl\n      }\n    }\n  }\n}`

async function load() {
  loading.value = true
  error.value = null
  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Temporary hardcoded auth header
        'authorization': 'bearer local-auth-token',
      },
      body: JSON.stringify({ query }),
      credentials: 'omit',
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const json = await res.json()
    if (json.errors) {
      throw new Error(json.errors?.[0]?.message || 'GraphQL error')
    }
    const data: Wikibase[] = json?.data?.wikibaseList?.data ?? []
    items.value = data
  } catch (e: any) {
    error.value = e?.message || String(e)
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <section>
    <div class="mb-4 flex items-center justify-between gap-4">
      <h2 class="text-2xl font-semibold">Wikibases</h2>
      <button
        type="button"
        class="rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white shadow hover:bg-indigo-500"
        @click="load()"
      >
        Refresh
      </button>
    </div>

    <div v-if="loading" class="text-gray-600 dark:text-gray-300">Loading…</div>
    <div v-else-if="error" class="text-red-600">{{ error }}</div>
    <div v-else>
      <p class="mb-3 text-sm text-gray-600 dark:text-gray-300">
        Found <span class="font-semibold">{{ items.length }}</span> wikibases
      </p>

      <div class="overflow-x-auto rounded-lg border border-gray-200 dark:border-neutral-700">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
          <thead class="bg-gray-50 dark:bg-neutral-800">
            <tr>
              <th class="px-4 py-2 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-neutral-300">ID</th>
              <th class="px-4 py-2 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:text-neutral-300">Base URL</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 bg-white dark:divide-neutral-800 dark:bg-neutral-900">
            <tr v-for="w in items" :key="w.id" class="hover:bg-gray-50 dark:hover:bg-neutral-800">
              <td class="px-4 py-2 text-sm text-gray-900 dark:text-neutral-100">{{ w.id }}</td>
              <td class="px-4 py-2 text-sm">
                <a
                  :href="w.urls?.baseUrl"
                  target="_blank"
                  rel="noreferrer noopener"
                  class="text-indigo-600 underline hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
                >
                  {{ w.urls?.baseUrl }}
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
  
</template>

<style scoped>
</style>
