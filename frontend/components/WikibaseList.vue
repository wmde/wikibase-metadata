<script setup lang="ts">
import { onMounted, ref } from "vue";
import {
	CdxButton,
	CdxCard,
	CdxInfoChip,
	CdxProgressBar,
	CdxTooltip,
} from "@wikimedia/codex";

type Wikibase = {
	id: string | number;
	urls: { baseUrl: string };
	wikibaseType?: string;
	description?: string;
	quantityObservations?: {
		mostRecent?: {
			observationDate?: string;
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

const endpoint = import.meta.env.DEV
	? "http://localhost:8000/graphql"
	: "/graphql";

const query = `query q {\n  wikibaseList(pageNumber: 1, pageSize: 1000000, wikibaseFilter: { wikibaseType: { exclude: [TEST, CLOUD] } }) {\n    data {\n      id\n      urls {\n        baseUrl\n      }\n      description\n      wikibaseType\n      quantityObservations {\n        mostRecent {\n          observationDate\n          totalItems\n          totalProperties\n          totalLexemes\n          totalTriples\n        }\n      }\n    }\n  }\n}`;

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

// Tooltip directive for Codex in <script setup>
const vTooltip = CdxTooltip;

function isStale(w: Wikibase): boolean {
	const d = w.quantityObservations?.mostRecent?.observationDate;
	if (!d) return false;
	const t = new Date(d).getTime();
	if (Number.isNaN(t)) return false;
	const THIRTY_DAYS = 30 * 24 * 60 * 60 * 1000;
	return Date.now() - t > THIRTY_DAYS;
}

function tooltipText(w: Wikibase): string {
	const d = w.quantityObservations?.mostRecent?.observationDate;
	if (!d) return "";
	const dt = new Date(d);
	const when = Number.isNaN(dt.getTime()) ? d : dt.toLocaleDateString();
	return `Measured more than 30 days ago`;
}
</script>

<template>
	<section>
		<div v-if="loading" class="py-6">
			<p class="mb-3 text-sm text-gray-600 dark:text-gray-300">
				Loading known Wikibase instances — this can take a while.
			</p>
			<CdxProgressBar aria-label="Loading known Wikibase instances" />
		</div>
		<div v-else-if="error" class="text-red-600">{{ error }}</div>
		<div v-else>
			<p class="mb-3 text-sm text-gray-600 dark:text-gray-300">
				Found
				<span class="font-semibold">{{ items.length }}</span> wikibases
			</p>

			<div
				class="grid grid-cols-1 items-stretch gap-4 sm:grid-cols-2 lg:grid-cols-3"
			>
				<div v-for="w in items" :key="w.id" class="h-full">
					<CdxCard class="flex h-full flex-col">
						<template #title>
							{{ hostOf(w.urls?.baseUrl) || "Unknown" }}
						</template>
						<template #description>
							<span
								v-if="w.wikibaseType"
								class="ml-2 rounded bg-gray-100 px-2 py-0.5 text-[10px] font-medium uppercase text-gray-700 dark:bg-neutral-800 dark:text-neutral-300"
								>{{ w.wikibaseType }}</span
							>
						</template>
						<template #supporting-text>
							<div class="flex flex-col h-full">
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
								</div>
								<div class="mt-2 flex flex-wrap gap-2 mt-auto">
									<CdxInfoChip
										:status="isStale(w) ? 'warning' : 'success'"
										v-tooltip="isStale(w) ? tooltipText(w) : null"
										v-if="
											w.quantityObservations?.mostRecent?.totalItems != null
										"
									>
										Items:
										{{ fmt(w.quantityObservations?.mostRecent?.totalItems) }}
									</CdxInfoChip>
									<CdxInfoChip
										:status="isStale(w) ? 'warning' : 'success'"
										v-tooltip="isStale(w) ? tooltipText(w) : null"
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
										:status="isStale(w) ? 'warning' : 'success'"
										v-tooltip="isStale(w) ? tooltipText(w) : null"
										v-if="
											w.quantityObservations?.mostRecent?.totalLexemes != null
										"
									>
										Lexemes:
										{{ fmt(w.quantityObservations?.mostRecent?.totalLexemes) }}
									</CdxInfoChip>
									<CdxInfoChip
										:status="isStale(w) ? 'warning' : 'success'"
										v-tooltip="isStale(w) ? tooltipText(w) : null"
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

<style scoped>
/* Ensure Codex card fills its grid cell and stacks content vertically */
:deep(.cdx-card) {
	height: 100%;
	display: flex;
	flex-direction: column;
}

/* Make the text area grow so supporting text can sit at the bottom */
:deep(.cdx-card__text) {
	display: flex;
	flex-direction: column;
	flex: 1 1 auto;
}
</style>
