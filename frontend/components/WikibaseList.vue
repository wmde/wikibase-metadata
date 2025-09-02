<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import {
	CdxButton,
	CdxCard,
	CdxToggleSwitch,
	CdxInfoChip,
	CdxProgressBar,
} from "@wikimedia/codex";

type Wikibase = {
	id: string | number;
	urls: { baseUrl: string };
	wikibaseType?: string;
	description?: string;
	quantityObservations?: {
		mostRecent?: {
			totalItems?: number;
			totalProperties?: number;
			totalLexemes?: number;
			totalTriples?: number;
		};
	};
};

const loading = ref(true);
const error = ref<string | null>(null);
const items = ref<Wikibase[]>([]);
const includeCloud = ref(false);
const displayedItems = computed(() =>
	includeCloud.value
		? items.value
		: items.value.filter(
				(w) => (w.wikibaseType || "").toUpperCase() !== "CLOUD",
			),
);

const endpoint = import.meta.env.DEV
	? "http://localhost:8000/graphql"
	: "/graphql";

const query = `query q {\n  wikibaseList(pageNumber: 1, pageSize: 1000000) {\n    data {\n      id\n      urls {\n        baseUrl\n      }\n      description\n      wikibaseType\n      quantityObservations {\n        mostRecent {\n          totalItems\n          totalProperties\n          totalLexemes\n          totalTriples\n        }\n      }\n    }\n  }\n}`;

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

const nf = new Intl.NumberFormat(undefined);
function fmt(n?: number | null) {
	if (n == null) return "";
	try {
		return nf.format(n as number);
	} catch {
		return String(n);
	}
}
</script>

<template>
	<section>
		<div
			class="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
		>
			<div class="max-w-xl">
				<CdxToggleSwitch v-model="includeCloud">
					Include cloud instances
					<template #description>
						Turn on to include wikibaseType "CLOUD" (e.g., wikibase.cloud).
					</template>
				</CdxToggleSwitch>
			</div>
			<div class="flex items-center justify-end gap-2">
				<CdxButton action="progressive" weight="primary" @click="load()">
					Refresh
				</CdxButton>
			</div>
		</div>

		<div v-if="loading" class="py-6">
			<CdxProgressBar aria-label="ProgressBar example" />
		</div>
		<div v-else-if="error" class="text-red-600">{{ error }}</div>
		<div v-else>
			<p class="mb-3 text-sm text-gray-600 dark:text-gray-300">
				Found
				<span class="font-semibold">{{ displayedItems.length }}</span> wikibases
			</p>

			<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
				<div v-for="w in displayedItems" :key="w.id" class="">
					<CdxCard>
						<template #title>
							{{ hostOf(w.urls?.baseUrl) || "Unknown" }}
						</template>
						<template #description>
							ID: {{ w.id
							}}<span
								v-if="w.wikibaseType"
								class="ml-2 rounded bg-gray-100 px-2 py-0.5 text-[10px] font-medium uppercase text-gray-700 dark:bg-neutral-800 dark:text-neutral-300"
								>{{ w.wikibaseType }}</span
							>
						</template>
						<template #supporting-text>
							<div>
								<a
									:href="w.urls?.baseUrl"
									target="_blank"
									rel="noreferrer noopener"
									class="text-indigo-600 underline hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
								>
									{{ w.urls?.baseUrl }}
								</a>
								<p
									v-if="w.description"
									class="mt-1 text-sm text-gray-600 dark:text-gray-300"
								>
									{{ w.description }}
								</p>
								<div class="mt-2 flex flex-wrap gap-2">
									<CdxInfoChip
										v-if="
											w.quantityObservations?.mostRecent?.totalItems != null
										"
									>
										Items:
										{{ fmt(w.quantityObservations?.mostRecent?.totalItems) }}
									</CdxInfoChip>
									<CdxInfoChip
										v-if="
											w.quantityObservations?.mostRecent?.totalProperties !=
											null
										"
									>
										Properties:
										{{
											fmt(w.quantityObservations?.mostRecent?.totalProperties)
										}}
									</CdxInfoChip>
									<CdxInfoChip
										v-if="
											w.quantityObservations?.mostRecent?.totalLexemes != null
										"
									>
										Lexemes:
										{{ fmt(w.quantityObservations?.mostRecent?.totalLexemes) }}
									</CdxInfoChip>
									<CdxInfoChip
										v-if="
											w.quantityObservations?.mostRecent?.totalTriples != null
										"
									>
										Triples:
										{{ fmt(w.quantityObservations?.mostRecent?.totalTriples) }}
									</CdxInfoChip>
								</div>
							</div>
						</template>
					</CdxCard>
				</div>
			</div>
		</div>
	</section>
</template>

<style scoped></style>
