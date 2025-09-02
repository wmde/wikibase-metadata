<script setup lang="ts">
import { onMounted, ref } from "vue";
import { CdxButton, CdxCard } from "@wikimedia/codex";

type Wikibase = {
	id: string | number;
	urls: { baseUrl: string };
};

const loading = ref(true);
const error = ref<string | null>(null);
const items = ref<Wikibase[]>([]);

const endpoint = import.meta.env.DEV
	? "http://localhost:8000/graphql"
	: "/graphql";

const query = `query q {\n  wikibaseList(pageNumber: 1, pageSize: 1000000) {\n    data {\n      id\n      urls {\n        baseUrl\n      }\n    }\n  }\n}`;

async function load() {
	loading.value = true;
	error.value = null;
	try {
		const res = await fetch(endpoint, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				// Temporary hardcoded auth header
				authorization: "bearer local-auth-token",
			},
			body: JSON.stringify({ query }),
			credentials: "omit",
		});
		if (!res.ok) throw new Error(`HTTP ${res.status}`);
		const json = await res.json();
		if (json.errors) {
			throw new Error(json.errors?.[0]?.message || "GraphQL error");
		}
		const data: Wikibase[] = json?.data?.wikibaseList?.data ?? [];
		items.value = data;
	} catch (e: any) {
		error.value = e?.message || String(e);
	} finally {
		loading.value = false;
	}
}

onMounted(load);

function hostOf(url?: string) {
  if (!url) return "";
  try {
    return new URL(url).host;
  } catch {
    return url;
  }
}
</script>

<template>
	<section>
		<div class="mb-4 flex items-center justify-end gap-4">
			<CdxButton action="progressive" weight="primary" @click="load()">
				Click me!
			</CdxButton>
		</div>

		<div v-if="loading" class="text-gray-600 dark:text-gray-300">Loading…</div>
		<div v-else-if="error" class="text-red-600">{{ error }}</div>
		<div v-else>
			<p class="mb-3 text-sm text-gray-600 dark:text-gray-300">
				Found <span class="font-semibold">{{ items.length }}</span> wikibases
			</p>

			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
				<div v-for="w in items" :key="w.id" class="">
					<CdxCard>
						<template #title>
							{{ hostOf(w.urls?.baseUrl) || 'Unknown' }}
						</template>
						<template #description>
							ID: {{ w.id }}
						</template>
						<template #supporting-text>
							<a
								:href="w.urls?.baseUrl"
								target="_blank"
								rel="noreferrer noopener"
								class="text-indigo-600 underline hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
							>
								{{ w.urls?.baseUrl }}
							</a>
						</template>
					</CdxCard>
				</div>
			</div>
		</div>
	</section>
</template>

<style scoped></style>
